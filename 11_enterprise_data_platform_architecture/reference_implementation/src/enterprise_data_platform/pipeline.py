"""Small metadata-driven Bronze/Silver/Gold reference pipeline."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .contracts import DataContract, validate_record
from .quality import (
    DataQualityError,
    allowed_values_rule,
    required_fields_rule,
    run_quality_checks,
    unique_grain_rule,
)


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: str | Path, payload: Any) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_pipeline(config_path: str | Path) -> dict[str, Any]:
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    contract = DataContract.load(config["contract_path"])
    rows = read_jsonl(config["input_path"])

    contract_errors = [
        {"row": index + 1, "errors": errors}
        for index, row in enumerate(rows)
        if (errors := validate_record(row, contract))
    ]
    if contract_errors:
        raise DataQualityError(f"Data contract violations: {contract_errors}")

    bronze = [
        {
            **row,
            "_ingested_at": datetime.now(timezone.utc).isoformat(),
            "_source_file": str(config["input_path"]),
        }
        for row in rows
    ]

    silver = []
    for row in bronze:
        silver.append(
            {
                **row,
                "domain": str(row["domain"]).strip().lower(),
                "status": str(row["status"]).strip().upper(),
                "amount": round(float(row["amount"]), 2),
            }
        )

    quality_results = run_quality_checks(
        silver,
        [
            required_fields_rule(["record_id", "domain", "status", "amount"]),
            unique_grain_rule(list(contract.grain)),
            allowed_values_rule("status", {"OPEN", "CLOSED"}),
        ],
    )

    gold_by_domain: dict[str, dict[str, Any]] = {}
    for row in silver:
        item = gold_by_domain.setdefault(
            row["domain"], {"domain": row["domain"], "record_count": 0, "total_amount": 0.0}
        )
        item["record_count"] += 1
        item["total_amount"] = round(item["total_amount"] + row["amount"], 2)
    gold = sorted(gold_by_domain.values(), key=lambda item: item["domain"])

    output_root = Path(config["output_root"])
    paths = {
        "bronze": output_root / "bronze.json",
        "silver": output_root / "silver.json",
        "gold": output_root / "gold.json",
        "quality": output_root / "quality_results.json",
        "lineage": output_root / "lineage_manifest.json",
        "run": output_root / "pipeline_run.json",
    }
    write_json(paths["bronze"], bronze)
    write_json(paths["silver"], silver)
    write_json(paths["gold"], gold)
    write_json(paths["quality"], quality_results)

    lineage = {
        "source": str(config["input_path"]),
        "source_sha256": _sha256(config["input_path"]),
        "contract": str(config["contract_path"]),
        "stages": ["bronze", "silver", "gold"],
        "outputs": {name: str(path) for name, path in paths.items() if name not in {"lineage", "run"}},
    }
    write_json(paths["lineage"], lineage)

    summary = {
        "status": "completed",
        "dataset": contract.dataset,
        "contract_version": contract.version,
        "input_rows": len(rows),
        "gold_rows": len(gold),
        "critical_quality_failures": 0,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "outputs": {name: str(path) for name, path in paths.items()},
    }
    write_json(paths["run"], summary)
    return summary
