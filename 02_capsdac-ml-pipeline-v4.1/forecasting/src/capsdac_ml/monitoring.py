from __future__ import annotations

from typing import Dict, Any
import numpy as np
import pandas as pd

from .feature_engineering import FEATURES

TEMPORAL_FEATURES = {"month_sin", "month_cos", "trend_index"}
BUSINESS_FEATURES = [f for f in FEATURES if f not in TEMPORAL_FEATURES] + ["EnrollmentCount"]


def population_stability_index(expected: pd.Series, actual: pd.Series, bins: int = 10) -> float:
    expected = pd.to_numeric(expected, errors="coerce").dropna()
    actual = pd.to_numeric(actual, errors="coerce").dropna()
    if expected.empty or actual.empty:
        return 0.0
    quantiles = np.unique(np.quantile(expected, np.linspace(0, 1, bins + 1)))
    if len(quantiles) < 3:
        return 0.0
    # Extend outer bounds so values outside the historical range are counted.
    quantiles[0], quantiles[-1] = -np.inf, np.inf
    exp_counts, _ = np.histogram(expected, bins=quantiles)
    act_counts, _ = np.histogram(actual, bins=quantiles)
    exp_pct = np.maximum(exp_counts / max(exp_counts.sum(), 1), 1e-6)
    act_pct = np.maximum(act_counts / max(act_counts.sum(), 1), 1e-6)
    return float(np.sum((act_pct - exp_pct) * np.log(act_pct / exp_pct)))


def _status(psi: float) -> str:
    return "high" if psi >= 0.25 else "moderate" if psi >= 0.10 else "stable"


def drift_report(feature_df: pd.DataFrame) -> Dict[str, Any]:
    """Monitor business/population drift separately from deterministic time features.

    Temporal encodings are reported for transparency but intentionally excluded from the
    operational drift trigger. Their distributions change as calendar time advances and
    should not, by themselves, force model retraining.
    """
    months = sorted(pd.to_datetime(feature_df["MonthDate"]).drop_duplicates())
    if len(months) < 4:
        return {"method": "population_stability_index", "overall_status": "insufficient_history", "features": []}
    split_idx = max(1, len(months) - 3)
    baseline_months, current_months = months[:split_idx], months[split_idx:]
    baseline = feature_df[feature_df["MonthDate"].isin(baseline_months)]
    current = feature_df[feature_df["MonthDate"].isin(current_months)]
    rows = []
    for feature in FEATURES + ["EnrollmentCount"]:
        psi = population_stability_index(baseline[feature], current[feature])
        rows.append({
            "feature": feature,
            "feature_group": "temporal_control" if feature in TEMPORAL_FEATURES else "business_population",
            "included_in_operational_status": feature not in TEMPORAL_FEATURES,
            "psi": psi,
            "status": _status(psi),
            "baseline_mean": float(baseline[feature].mean()),
            "current_mean": float(current[feature].mean()),
        })
    operational = [r for r in rows if r["included_in_operational_status"]]
    overall = "high" if any(r["status"] == "high" for r in operational) else "moderate" if any(r["status"] == "moderate" for r in operational) else "stable"
    return {
        "baseline_start": baseline_months[0].strftime("%Y-%m"),
        "baseline_end": baseline_months[-1].strftime("%Y-%m"),
        "current_start": current_months[0].strftime("%Y-%m"),
        "current_end": current_months[-1].strftime("%Y-%m"),
        "method": "population_stability_index",
        "thresholds": {"stable": "<0.10", "moderate": "0.10-0.25", "high": ">=0.25"},
        "policy": "Operational status uses business/population features only; deterministic calendar/trend features are diagnostic only.",
        "features": rows,
        "overall_status": overall,
    }
