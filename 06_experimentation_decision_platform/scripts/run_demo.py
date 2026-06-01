from pathlib import Path
import pandas as pd
from experiment_platform.data_contracts import ExperimentContract
from experiment_platform.cuped import apply_cuped
from experiment_platform.ab_testing import t_test
from experiment_platform.bayesian import beta_binomial_ab
from experiment_platform.uplift import train_t_learner
from experiment_platform.reporting import build_executive_report

root = Path(__file__).resolve().parents[1]
data_path = root / "data" / "sample_experiment.csv"
if not data_path.exists():
    raise SystemExit("Run scripts/generate_sample_data.py first")
df = pd.read_csv(data_path)
ExperimentContract().validate(df)
df = apply_cuped(df, "post_period_metric", "pre_period_metric")
ab = t_test(df, "post_period_metric_cuped")
bayes = beta_binomial_ab(df)
uplift = train_t_learner(df)
report = build_executive_report(ab, bayes, uplift)
out = root / "outputs" / "executive_experiment_report.md"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(report, encoding="utf-8")
print(report)
