"""Frequentist two-arm experiment estimators."""
from __future__ import annotations

import numpy as np
import pandas as pd


def difference_in_means(
    df: pd.DataFrame,
    outcome: str,
    treatment_col: str = "treatment",
) -> dict[str, float | list[float] | int]:
    """Estimate an unadjusted treatment-control mean difference and 95% CI."""
    missing = {outcome, treatment_col} - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    treatment = df.loc[df[treatment_col] == 1, outcome].dropna().astype(float)
    control = df.loc[df[treatment_col] == 0, outcome].dropna().astype(float)
    if len(treatment) < 2 or len(control) < 2:
        raise ValueError("Each experiment arm must contain at least two observations")

    control_mean = float(control.mean())
    treatment_mean = float(treatment.mean())
    lift = treatment_mean - control_mean
    standard_error = float(
        np.sqrt(treatment.var(ddof=1) / len(treatment) + control.var(ddof=1) / len(control))
    )
    return {
        "control_mean": control_mean,
        "treatment_mean": treatment_mean,
        "absolute_lift": lift,
        "relative_lift_pct": float(lift / control_mean * 100) if control_mean else 0.0,
        "standard_error": standard_error,
        "ci_95": [lift - 1.96 * standard_error, lift + 1.96 * standard_error],
        "n_control": int(len(control)),
        "n_treatment": int(len(treatment)),
    }
