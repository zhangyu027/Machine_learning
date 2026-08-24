from __future__ import annotations

import numpy as np
import pandas as pd

# V4 is deliberately calibrated to one year of history. A 12-month lag is not
# used because it would leave almost no temporal holdout data with only 12 months.
FEATURES = [
    "enrollment_t",
    "lag_1",
    "lag_2",
    "lag_3",
    "rolling_3",
    "month_sin",
    "month_cos",
    "trend_index",
    "ft_share",
    "iep_share",
    "dll_share",
    "homeless_eligibility_share",
    "median_family_monthly_income",
    "mean_family_size",
    "agency_enrollment",
    "agency_active_sites",
]

TARGET_COL = "TargetEnrollmentH1"
FORECAST_HORIZON_MONTHS = 1


def _fill_context_by_site(out: pd.DataFrame, column: str, default: float = 0.0) -> pd.Series:
    numeric = pd.to_numeric(out[column], errors="coerce") if column in out.columns else pd.Series(np.nan, index=out.index)
    by_site = numeric.groupby(out["PreschoolCDSCode"]).transform(lambda s: s.ffill().bfill())
    global_median = float(numeric.median()) if numeric.notna().any() else default
    return by_site.fillna(global_median).fillna(default)


def build_monthly_features(df: pd.DataFrame, horizon_months: int = FORECAST_HORIZON_MONTHS) -> pd.DataFrame:
    """Build leakage-safe site-month features from 12 months of CAPSDAC aggregates.

    The default target is one month ahead. With exactly twelve months, this gives
    enough distinct holdout months for expanding-window evaluation while still
    using short-term seasonality and site history. The horizon is configurable,
    but longer horizons require more historical months for a defensible CV design.
    """
    out = df.copy()
    if "MonthDate" not in out.columns:
        out["MonthDate"] = pd.to_datetime(out["SnapshotMonth"] + "-01", errors="raise")
    else:
        out["MonthDate"] = pd.to_datetime(out["MonthDate"], errors="raise")

    out = out.sort_values(["PreschoolCDSCode", "MonthDate"]).reset_index(drop=True)
    site_group = out.groupby("PreschoolCDSCode", group_keys=False)

    out["enrollment_t"] = pd.to_numeric(out["EnrollmentCount"], errors="coerce")
    for lag in [1, 2, 3]:
        out[f"lag_{lag}"] = site_group["EnrollmentCount"].shift(lag)

    out["rolling_3"] = site_group["EnrollmentCount"].transform(
        lambda s: s.shift(1).rolling(window=3, min_periods=3).mean()
    )

    out["month"] = out["MonthDate"].dt.month
    out["month_sin"] = np.sin(2 * np.pi * out["month"] / 12)
    out["month_cos"] = np.cos(2 * np.pi * out["month"] / 12)
    min_month = out["MonthDate"].min()
    out["trend_index"] = (out["MonthDate"].dt.year - min_month.year) * 12 + (out["MonthDate"].dt.month - min_month.month)

    context_map = {
        "ft_share": "FTShare",
        "iep_share": "IEPShare",
        "dll_share": "DLLShare",
        "homeless_eligibility_share": "HomelessEligibilityShare",
        "median_family_monthly_income": "MedianFamilyMonthlyIncome",
        "mean_family_size": "MeanFamilySize",
        "agency_enrollment": "AgencyEnrollment",
        "agency_active_sites": "AgencyActiveSites",
    }
    for feature_name, source_col in context_map.items():
        out[feature_name] = _fill_context_by_site(out, source_col)

    out[TARGET_COL] = site_group["EnrollmentCount"].shift(-horizon_months)
    out["TargetMonth"] = (out["MonthDate"] + pd.DateOffset(months=horizon_months)).dt.strftime("%Y-%m")

    required = FEATURES + [TARGET_COL]
    return out.dropna(subset=required).reset_index(drop=True)
