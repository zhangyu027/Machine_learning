"""Sequential Bayesian experiment monitoring."""
from __future__ import annotations

import pandas as pd

from .bayesian_ab_test import beta_binomial_ab_test


def sequential_conversion_monitor(
    df: pd.DataFrame,
    day_col: str = "event_day",
    treatment_col: str = "treatment",
    outcome_col: str = "converted",
    draws: int = 20_000,
) -> pd.DataFrame:
    """Calculate cumulative Bayesian evidence at each observed experiment day."""
    missing = {day_col, treatment_col, outcome_col} - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    rows: list[dict[str, object]] = []
    for day in sorted(df[day_col].dropna().unique()):
        current = df[df[day_col] <= day]
        success_t = int(current.loc[current[treatment_col] == 1, outcome_col].sum())
        n_t = int((current[treatment_col] == 1).sum())
        success_c = int(current.loc[current[treatment_col] == 0, outcome_col].sum())
        n_c = int((current[treatment_col] == 0).sum())
        if n_t and n_c:
            result = beta_binomial_ab_test(
                success_t, n_t, success_c, n_c, draws=draws, seed=int(day)
            )
            rows.append({"day": int(day), "n_treatment": n_t, "n_control": n_c, **result})
    return pd.DataFrame(rows)
