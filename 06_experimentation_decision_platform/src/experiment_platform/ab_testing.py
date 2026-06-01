from __future__ import annotations
import numpy as np
import pandas as pd
from scipy import stats


def summarize_by_variant(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    return (
        df.groupby("variant")[metric]
        .agg(count="count", mean="mean", std="std")
        .reset_index()
    )


def t_test(df: pd.DataFrame, metric: str = "post_period_metric") -> dict:
    control = df.loc[df.variant == "control", metric].astype(float)
    treatment = df.loc[df.variant == "treatment", metric].astype(float)
    stat, p_value = stats.ttest_ind(treatment, control, equal_var=False)
    lift = treatment.mean() - control.mean()
    relative_lift = lift / control.mean() if control.mean() != 0 else np.nan
    return {
        "metric": metric,
        "control_mean": float(control.mean()),
        "treatment_mean": float(treatment.mean()),
        "absolute_lift": float(lift),
        "relative_lift": float(relative_lift),
        "t_stat": float(stat),
        "p_value": float(p_value),
        "is_significant_05": bool(p_value < 0.05),
    }


def conversion_z_test(df: pd.DataFrame) -> dict:
    c = df[df.variant == "control"]
    t = df[df.variant == "treatment"]
    p1, p2 = c.converted.mean(), t.converted.mean()
    n1, n2 = len(c), len(t)
    pooled = (c.converted.sum() + t.converted.sum()) / (n1 + n2)
    se = np.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se if se > 0 else np.nan
    p_value = 2 * (1 - stats.norm.cdf(abs(z))) if np.isfinite(z) else np.nan
    return {"control_rate": float(p1), "treatment_rate": float(p2), "lift": float(p2-p1), "z": float(z), "p_value": float(p_value)}
