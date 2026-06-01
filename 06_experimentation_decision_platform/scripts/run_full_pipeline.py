import json
from pathlib import Path
import pandas as pd
from src.experimentation.ab_test import difference_in_means
from src.experimentation.cuped import apply_cuped
from src.experimentation.bayesian_ab_test import beta_binomial_ab_test

ROOT = Path(__file__).resolve().parents[1]

def main():
    df = pd.read_csv(ROOT / "data/raw/experiment_events.csv")
    df["cuped_revenue"] = apply_cuped(df, "post_period_revenue", "pre_period_revenue")
    results = {
        "post_period_revenue": difference_in_means(df, "post_period_revenue"),
        "cuped_revenue": difference_in_means(df, "cuped_revenue"),
        "converted": difference_in_means(df, "converted"),
    }
    st = int(df.loc[df.treatment == 1, "converted"].sum())
    nt = int((df.treatment == 1).sum())
    sc = int(df.loc[df.treatment == 0, "converted"].sum())
    nc = int((df.treatment == 0).sum())
    results["bayesian_conversion_test"] = beta_binomial_ab_test(st, nt, sc, nc)
    (ROOT / "data/processed/experiment_analysis_dataset.csv").parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ROOT / "data/processed/experiment_analysis_dataset.csv", index=False)
    (ROOT / "reports/model_outputs/executive_decision_report.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
