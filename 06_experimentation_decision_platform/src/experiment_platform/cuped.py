from __future__ import annotations
import pandas as pd


def apply_cuped(df: pd.DataFrame, outcome_col: str, covariate_col: str) -> pd.DataFrame:
    """CUPED adjustment: Y_adj = Y - theta * (X - mean(X))."""
    out = df.copy()
    cov = out[covariate_col].astype(float)
    y = out[outcome_col].astype(float)
    theta = cov.cov(y) / cov.var() if cov.var() != 0 else 0.0
    out[f"{outcome_col}_cuped"] = y - theta * (cov - cov.mean())
    out["cuped_theta"] = theta
    return out
