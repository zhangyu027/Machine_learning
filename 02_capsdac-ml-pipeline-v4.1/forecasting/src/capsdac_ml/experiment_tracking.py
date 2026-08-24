from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import uuid

import pandas as pd


def write_experiment_artifacts(root: Path, leaderboard: pd.DataFrame, selection_report: dict, package_level: str = "V4.1 Senior Data Scientist / MLE Decision Science") -> dict:
    run_id = f"capsdac-v4.1-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
    exp_dir = root / "outputs" / "experiments" / run_id
    exp_dir.mkdir(parents=True, exist_ok=True)
    leaderboard.to_csv(exp_dir / "leaderboard.csv", index=False)
    (exp_dir / "selection_report.json").write_text(json.dumps(selection_report, indent=2))
    metadata = {
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "package_level": package_level,
        "tracking_mode": "local_file_mlflow_style",
        "selection_metric": "rmse",
        "selected_model": selection_report["selected_model"]["model_name"],
        "selected_params": selection_report["selected_model"]["params"],
        "selected_metrics": selection_report["selected_model"]["avg_metrics"],
        "artifact_uri": str(exp_dir.relative_to(root)),
    }
    (exp_dir / "run_metadata.json").write_text(json.dumps(metadata, indent=2))

    registry_path = root / "outputs" / "experiments" / "runs.csv"
    row = pd.DataFrame([metadata])
    if registry_path.exists():
        runs = pd.concat([pd.read_csv(registry_path), row], ignore_index=True)
    else:
        runs = row
    runs.to_csv(registry_path, index=False)
    return metadata
