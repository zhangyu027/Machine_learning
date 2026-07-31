"""CUPED variance reduction."""
from __future__ import annotations

import numpy as np
import pandas as pd


def apply_cuped(df: pd.DataFrame, outcome: str, pre_period_metric: str) -> pd.Series:
    """Return a CUPED-adjusted outcome using a pre-experiment covariate."""
    missing = {outcome, pre_period_metric} - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    outcome_values = df[outcome].astype(float)
    covariate = df[pre_period_metric].astype(float)
    variance = float(np.var(covariate, ddof=0))
    if not np.isfinite(variance) or variance <= 0:
        raise ValueError("CUPED pre-period metric must have positive variance")
    covariance = float(np.cov(outcome_values, covariate, ddof=0)[0, 1])
    theta = covariance / variance
    return outcome_values - theta * (covariate - covariate.mean())
