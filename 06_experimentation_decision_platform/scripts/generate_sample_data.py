from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 5000
variant = rng.choice(["control", "treatment"], size=n)
segment = rng.choice(["new", "returning", "high_value"], p=[.45,.40,.15], size=n)
age = rng.integers(18, 75, size=n)
engagement = rng.normal(50, 12, size=n).clip(0, 100)
pre = rng.normal(100, 20, size=n)
true_lift = np.where(segment == "high_value", 10, np.where(segment == "returning", 5, 2))
post = pre * 0.55 + rng.normal(45, 10, size=n) + np.where(variant == "treatment", true_lift, 0)
logit = -2.2 + 0.015*engagement + np.where(variant == "treatment", .25, 0) + np.where(segment == "high_value", .35, 0)
prob = 1/(1+np.exp(-logit))
converted = rng.binomial(1, prob)
df = pd.DataFrame({"user_id": range(n), "variant": variant, "segment": segment, "age": age, "engagement_score": engagement, "pre_period_metric": pre, "post_period_metric": post, "converted": converted})
out = Path(__file__).resolve().parents[1] / "data" / "sample_experiment.csv"
out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out, index=False)
print(out)
