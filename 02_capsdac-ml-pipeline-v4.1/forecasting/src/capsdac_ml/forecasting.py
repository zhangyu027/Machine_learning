from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.base import RegressorMixin

from .feature_engineering import FEATURES, FORECAST_HORIZON_MONTHS


def generate_site_forecast(model: RegressorMixin, feature_df: pd.DataFrame, horizon_months: int = FORECAST_HORIZON_MONTHS) -> pd.DataFrame:
    """Generate site-level next-month forecasts from each site's latest usable row."""
    latest = feature_df.sort_values(["PreschoolCDSCode", "MonthDate"]).groupby("PreschoolCDSCode", as_index=False).tail(1).copy()
    latest["ForecastMonth"] = (latest["MonthDate"] + pd.DateOffset(months=horizon_months)).dt.strftime("%Y-%m")
    latest["ForecastHorizonMonths"] = horizon_months
    latest["PredictedEnrollment"] = model.predict(latest[FEATURES]).round().clip(min=0).astype(int)
    latest["CurrentEnrollment"] = latest["enrollment_t"].round().astype(int)
    latest["ForecastChange"] = latest["PredictedEnrollment"] - latest["CurrentEnrollment"]
    latest["ForecastPctChange"] = latest["ForecastChange"] / latest["CurrentEnrollment"].clip(lower=1)
    latest["OperationalReviewFlag"] = latest["ForecastPctChange"].abs() >= 0.20
    cols = [
        "ForecastMonth", "ForecastHorizonMonths", "VendorNumber", "LEAName", "PreschoolCDSCode", "SiteName",
        "County", "FundingType", "CurrentEnrollment", "PredictedEnrollment", "ForecastChange", "ForecastPctChange",
        "OperationalReviewFlag",
    ]
    return latest[cols].sort_values(["ForecastMonth", "VendorNumber", "PreschoolCDSCode"]).reset_index(drop=True)


def save_model(model: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
