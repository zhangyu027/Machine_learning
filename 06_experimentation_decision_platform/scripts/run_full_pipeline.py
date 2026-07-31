"""Run the complete experimentation decision workflow."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from bandits.thompson_sampling import simulate_thompson_sampling
from causal.uplift_t_learner import TLearnerUpliftModel
from experimentation.ab_test import difference_in_means
from experimentation.bayesian_ab_test import beta_binomial_ab_test
from experimentation.cuped import apply_cuped


def build_decision(probability: float, expected_lift: float) -> str:
    """Map posterior evidence to a conservative portfolio decision label."""
    if probability >= 0.95 and expected_lift > 0:
        return "ship"
    if probability <= 0.05 and expected_lift < 0:
        return "do_not_ship"
    return "continue_experiment"


def main() -> dict[str, object]:
    raw_path = ROOT / "data" / "raw" / "experiment_events.csv"
    if not raw_path.exists():
        raise FileNotFoundError(f"Input dataset not found: {raw_path}")
    df = pd.read_csv(raw_path)
    df["cuped_revenue"] = apply_cuped(df, "post_period_revenue", "pre_period_revenue")

    results: dict[str, object] = {
        "project": "06_experimentation_decision_platform",
        "pipeline_status": "completed_successfully",
        "observations": int(len(df)),
        "frequentist": {
            "post_period_revenue": difference_in_means(df, "post_period_revenue"),
            "cuped_revenue": difference_in_means(df, "cuped_revenue"),
            "converted": difference_in_means(df, "converted"),
        },
    }
    success_t = int(df.loc[df.treatment == 1, "converted"].sum())
    n_t = int((df.treatment == 1).sum())
    success_c = int(df.loc[df.treatment == 0, "converted"].sum())
    n_c = int((df.treatment == 0).sum())
    bayesian = beta_binomial_ab_test(success_t, n_t, success_c, n_c)
    results["bayesian_conversion_test"] = bayesian
    results["decision"] = build_decision(
        float(bayesian["prob_treatment_better"]), float(bayesian["expected_lift"])
    )

    feature_columns = ["customer_age", "prior_spend_30d", "prior_visits_30d", "pre_period_revenue"]
    model = TLearnerUpliftModel().fit(df[feature_columns], df["post_period_revenue"], df["treatment"])
    df["estimated_cate"] = model.predict_cate(df[feature_columns])
    bandit = simulate_thompson_sampling(
        [success_c / n_c, success_t / n_t], steps=2_000, snapshot_every=100
    )

    processed_dir = ROOT / "data" / "processed"
    output_dir = ROOT / "reports" / "model_outputs"
    model_dir = ROOT / "models"
    for directory in (processed_dir, output_dir, model_dir):
        directory.mkdir(parents=True, exist_ok=True)
    df.to_csv(processed_dir / "experiment_analysis_dataset.csv", index=False)
    df[["user_id", "treatment", "estimated_cate"]].to_csv(output_dir / "uplift_scores.csv", index=False)
    bandit.to_csv(output_dir / "thompson_sampling_bandit.csv", index=False)
    joblib.dump(model, model_dir / "uplift_t_learner.joblib")
    (output_dir / "executive_decision_report.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
