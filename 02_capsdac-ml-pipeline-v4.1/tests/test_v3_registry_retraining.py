from pathlib import Path
import json

from src.capsdac_ml.retraining import retraining_decision


def test_retraining_decision_creates_policy_file(tmp_path: Path):
    metrics = {"time_series_cv_avg_metrics": {"rmse": 1.0}}
    drift = {"overall_status": "stable"}
    decision = retraining_decision(tmp_path, metrics, drift)
    assert decision["retraining_policy"] == "monthly_challenger_training_with_champion_comparison"
    assert (tmp_path / "outputs/retraining/retraining_decision.json").exists()
    saved = json.loads((tmp_path / "outputs/retraining/retraining_decision.json").read_text())
    assert "new_month_workflow" in saved
