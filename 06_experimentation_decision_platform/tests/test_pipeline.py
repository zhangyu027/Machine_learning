from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from scripts import run_full_pipeline


def test_pipeline_writes_expected_artifacts(monkeypatch, tmp_path: Path) -> None:
    rng = np.random.default_rng(42)
    n = 400

    treatment = np.tile([0, 1], n // 2)
    customer_age = rng.integers(18, 70, size=n)
    prior_spend = rng.uniform(5, 100, size=n)
    prior_visits = rng.integers(0, 15, size=n)
    pre_revenue = prior_spend + rng.normal(0, 5, size=n)

    frame = pd.DataFrame(
        {
            "user_id": np.arange(n),
            "treatment": treatment,
            "customer_age": customer_age,
            "prior_spend_30d": prior_spend,
            "prior_visits_30d": prior_visits,
            "pre_period_revenue": pre_revenue,
            "post_period_revenue": (
                5 + 0.8 * pre_revenue + 2 * treatment + rng.normal(0, 5, size=n)
            ),
            "converted": rng.binomial(1, 0.5 + 0.1 * treatment),
        }
    )

    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    frame.to_csv(raw_dir / "experiment_events.csv", index=False)

    monkeypatch.setattr(run_full_pipeline, "ROOT", tmp_path)

    result = run_full_pipeline.main()

    assert result["pipeline_status"] == "completed_successfully"

    report = tmp_path / "reports" / "model_outputs" / "executive_decision_report.json"
    assert report.exists()
    assert json.loads(report.read_text())["decision"] in {
        "ship",
        "do_not_ship",
        "continue_experiment",
    }
    assert (tmp_path / "models" / "uplift_t_learner.joblib").exists()
