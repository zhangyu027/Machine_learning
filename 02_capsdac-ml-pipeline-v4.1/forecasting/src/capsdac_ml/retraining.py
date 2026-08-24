from __future__ import annotations

from pathlib import Path
import json


def retraining_decision(root: Path, model_metrics: dict, drift_report: dict, rmse_threshold: float = 2.0) -> dict:
    selected = model_metrics["time_series_cv_avg_metrics"]
    drift_status = drift_report.get("overall_status", "unknown")
    should_retrain = drift_status in {"moderate", "high"} or float(selected.get("rmse", 0)) > rmse_threshold
    decision = {
        "retraining_policy": "monthly_challenger_training_with_champion_comparison",
        "triggered": bool(should_retrain),
        "trigger_reasons": [],
        "new_month_workflow": [
            "ingest_new_snapshot",
            "validate_data_contracts",
            "rebuild_feature_store",
            "train_challenger_models",
            "compare_against_champion",
            "promote_or_reject",
            "publish_forecasts_and_monitoring_report",
        ],
        "production_note": "In production this would be scheduled by Airflow/Cloud Composer or GitHub Actions and registered in MLflow/Vertex AI.",
    }
    if drift_status in {"moderate", "high"}:
        decision["trigger_reasons"].append(f"Data drift status is {drift_status}.")
    if float(selected.get("rmse", 0)) > rmse_threshold:
        decision["trigger_reasons"].append("Validation RMSE exceeded threshold.")
    if not decision["trigger_reasons"]:
        decision["trigger_reasons"].append("Routine monthly retraining candidate; no emergency trigger.")

    out_path = root / "outputs" / "retraining" / "retraining_decision.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(decision, indent=2))
    return decision
