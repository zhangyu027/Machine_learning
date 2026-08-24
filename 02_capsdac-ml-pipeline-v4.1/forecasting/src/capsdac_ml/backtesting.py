from __future__ import annotations

from typing import Any, Dict
import numpy as np
import pandas as pd
from sklearn.base import clone

from .feature_engineering import FEATURES, TARGET_COL
from .model_selection import expanding_window_splits, regression_metrics


def rolling_backtest(feature_df: pd.DataFrame, model: Any, min_train_months: int = 4) -> pd.DataFrame:
    """Evaluate the selected model and persistence/moving-average baselines month by month."""
    rows = []
    for fold, split in enumerate(expanding_window_splits(feature_df, min_train_months=min_train_months), start=1):
        train = feature_df.loc[split["train_mask"]]
        test = feature_df.loc[split["test_mask"]]
        fitted = clone(model)
        fitted.fit(train[FEATURES], train[TARGET_COL])
        predictions = {
            "champion": fitted.predict(test[FEATURES]),
            "persistence_baseline": test["enrollment_t"].to_numpy(),
            "moving_average_3_baseline": test["rolling_3"].to_numpy(),
        }
        for name, pred in predictions.items():
            m = regression_metrics(test[TARGET_COL], pred)
            rows.append({"fold": fold, "test_month": split["test_start"], "model": name, **m})
    return pd.DataFrame(rows)


def backtest_summary(backtest: pd.DataFrame) -> Dict[str, Any]:
    summary = {}
    for name, g in backtest.groupby("model"):
        summary[name] = {f"{metric}_{stat}": float(getattr(g[metric], stat)()) for metric in ["mae", "rmse", "mape", "r2"] for stat in ["mean", "std"]}
    champion = summary.get("champion", {})
    persistence = summary.get("persistence_baseline", {})
    p_rmse = persistence.get("rmse_mean")
    c_rmse = champion.get("rmse_mean")
    improvement = None if not p_rmse else (p_rmse - c_rmse) / p_rmse * 100
    return {"models": summary, "champion_rmse_improvement_vs_persistence_pct": improvement}
