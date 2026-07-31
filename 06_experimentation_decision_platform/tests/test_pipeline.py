from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from scripts import run_full_pipeline


def test_pipeline_writes_expected_artifacts(monkeypatch, tmp_path: Path) -> None:
    source = Path(__file__).parents[1] / "data" / "raw" / "experiment_events.csv"
    frame = pd.read_csv(source, nrows=400)
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    frame.to_csv(raw_dir / "experiment_events.csv", index=False)
    monkeypatch.setattr(run_full_pipeline, "ROOT", tmp_path)
    result = run_full_pipeline.main()
    assert result["pipeline_status"] == "completed_successfully"
    report = tmp_path / "reports" / "model_outputs" / "executive_decision_report.json"
    assert report.exists()
    assert json.loads(report.read_text())["decision"] in {"ship", "do_not_ship", "continue_experiment"}
    assert (tmp_path / "models" / "uplift_t_learner.joblib").exists()
