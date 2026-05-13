"""
CAPSDAC forecasting utilities.

This file is designed to support 3-5 month recursive enrollment forecasting.
The notebook contains the full analysis; this module provides reusable logic.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor


def create_lag_features(df, group_col, time_col, target_col, lags=(1, 2, 3)):
    """
    Create lag features for recursive time-series forecasting.
    """
    out = df.sort_values([group_col, time_col]).copy()

    for lag in lags:
        out[f"{target_col}_lag_{lag}"] = out.groupby(group_col)[target_col].shift(lag)

    return out


def train_random_forest_forecaster(train_df, feature_cols, target_col):
    """
    Train a simple RandomForestRegressor forecaster.
    """
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        min_samples_leaf=2,
    )
    model.fit(train_df[feature_cols], train_df[target_col])
    return model


def summarize_forecast_by_group(df, group_col, forecast_col):
    """
    Summarize forecasted enrollment by group.
    """
    return (
        df.groupby(group_col, as_index=False)[forecast_col]
        .sum()
        .sort_values(forecast_col, ascending=False)
    )
