from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import shutil
from typing import Any

import joblib


def promote_champion_model(root: Path, model: Any, run_metadata: dict, challenger_metrics: dict) -> dict:
    registry_dir = root / "models" / "registry"
    registry_dir.mkdir(parents=True, exist_ok=True)
    champion_path = registry_dir / "champion_model.joblib"
    challenger_path = registry_dir / "latest_challenger_model.joblib"
    joblib.dump(model, challenger_path)

    prior = None
    registry_json = registry_dir / "model_registry.json"
    if registry_json.exists():
        prior = json.loads(registry_json.read_text())

    decision = "promoted"
    reason = "No existing champion, promoted first V4.1 champion."
    if prior and prior.get("champion_metrics"):
        prior_rmse = float(prior["champion_metrics"].get("rmse", 1e9))
        new_rmse = float(challenger_metrics.get("rmse", 1e9))
        if new_rmse <= prior_rmse * 1.02:
            decision = "promoted"
            reason = "Challenger RMSE is within acceptance threshold versus existing champion."
        else:
            decision = "rejected"
            reason = "Challenger RMSE degraded by more than 2% versus existing champion."

    if decision == "promoted":
        shutil.copyfile(challenger_path, champion_path)

    record = {
        "registry_version": "capsdac-v4.1-registry-1",
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "decision_reason": reason,
        "champion_model_uri": str(champion_path.relative_to(root)) if champion_path.exists() else None,
        "challenger_model_uri": str(challenger_path.relative_to(root)),
        "champion_run_id": run_metadata["run_id"] if decision == "promoted" else (prior or {}).get("champion_run_id"),
        "champion_model_name": run_metadata["selected_model"] if decision == "promoted" else (prior or {}).get("champion_model_name"),
        "champion_metrics": challenger_metrics if decision == "promoted" else (prior or {}).get("champion_metrics"),
        "latest_challenger": {"run_id": run_metadata["run_id"], "model_name": run_metadata["selected_model"], "metrics": challenger_metrics},
    }
    registry_json.write_text(json.dumps(record, indent=2))
    return record
