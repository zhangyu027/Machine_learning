from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import ParameterGrid
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .feature_engineering import FEATURES, TARGET_COL


def regression_metrics(y_true, y_pred) -> Dict[str, float]:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(math.sqrt(mean_squared_error(y_true, y_pred))),
        "mape": float(np.mean(np.abs((y_true - y_pred) / np.maximum(np.abs(y_true), 1))) * 100),
        "r2": float(r2_score(y_true, y_pred)) if len(np.unique(y_true)) > 1 else 0.0,
    }


def make_candidate_models(random_state: int = 2026) -> Dict[str, tuple[Any, Dict[str, list[Any]]]]:
    return {
        "median_baseline": (DummyRegressor(strategy="median"), {}),
        "linear_regression": (Pipeline([("scaler", StandardScaler()), ("model", LinearRegression())]), {}),
        "ridge_regression": (
            Pipeline([("scaler", StandardScaler()), ("model", Ridge())]),
            {"model__alpha": [0.1, 1.0, 10.0]},
        ),
        "random_forest": (
            RandomForestRegressor(random_state=random_state, n_jobs=-1),
            {"n_estimators": [120], "max_depth": [8, 12], "min_samples_leaf": [1, 3]},
        ),
        "gradient_boosting": (
            GradientBoostingRegressor(random_state=random_state),
            {"n_estimators": [100], "learning_rate": [0.05], "max_depth": [2, 3]},
        ),
        "extra_trees": (
            ExtraTreesRegressor(random_state=random_state, n_jobs=-1),
            {"n_estimators": [120], "max_depth": [8, 12], "min_samples_leaf": [1, 3]},
        ),
    }


def expanding_window_splits(feature_df: pd.DataFrame, min_train_months: int = 4, validation_months: int = 1) -> List[Dict[str, Any]]:
    months = sorted(pd.to_datetime(feature_df["MonthDate"]).drop_duplicates())
    splits: List[Dict[str, Any]] = []
    for test_start_idx in range(min_train_months, len(months) - validation_months + 1):
        train_months = months[:test_start_idx]
        test_months = months[test_start_idx : test_start_idx + validation_months]
        splits.append(
            {
                "train_start": train_months[0].strftime("%Y-%m"),
                "train_end": train_months[-1].strftime("%Y-%m"),
                "test_start": test_months[0].strftime("%Y-%m"),
                "test_end": test_months[-1].strftime("%Y-%m"),
                "train_mask": feature_df["MonthDate"].isin(train_months),
                "test_mask": feature_df["MonthDate"].isin(test_months),
            }
        )
    if not splits:
        raise ValueError(
            f"Not enough feature months for expanding-window validation: {len(months)} available. "
            "Provide more history or reduce feature lag depth."
        )
    return splits


def evaluate_model_class(feature_df: pd.DataFrame, name: str, estimator: Any, params: Dict[str, Any], splits: List[Dict[str, Any]]) -> Dict[str, Any]:
    fold_rows = []
    for fold_num, split in enumerate(splits, start=1):
        model = clone(estimator) if hasattr(estimator, "get_params") else estimator
        if hasattr(model, "set_params"):
            model.set_params(**params)
        train = feature_df.loc[split["train_mask"]]
        test = feature_df.loc[split["test_mask"]]
        model.fit(train[FEATURES], train[TARGET_COL])
        pred = model.predict(test[FEATURES])
        m = regression_metrics(test[TARGET_COL], pred)
        fold_rows.append({"fold": fold_num, **{k: v for k, v in split.items() if not k.endswith("mask")}, **m})
    avg = {k: float(np.mean([r[k] for r in fold_rows])) for k in ["mae", "rmse", "mape", "r2"]}
    return {"model_name": name, "params": params, "avg_metrics": avg, "folds": fold_rows}


def run_model_selection(feature_df: pd.DataFrame, max_param_sets_per_model: int = 4) -> Tuple[Any, Dict[str, Any], pd.DataFrame]:
    splits = expanding_window_splits(feature_df)
    candidates = make_candidate_models()
    results = []
    best_score = float("inf")
    best_record: Dict[str, Any] | None = None

    for name, (estimator, grid) in candidates.items():
        param_sets = list(ParameterGrid(grid)) if grid else [{}]
        for params in param_sets[:max_param_sets_per_model]:
            record = evaluate_model_class(feature_df, name, estimator, params, splits)
            results.append(record)
            if record["avg_metrics"]["rmse"] < best_score:
                best_score = record["avg_metrics"]["rmse"]
                best_record = record

    assert best_record is not None
    base_estimator = candidates[best_record["model_name"]][0]
    best_model = clone(base_estimator) if hasattr(base_estimator, "get_params") else base_estimator
    if hasattr(best_model, "set_params"):
        best_model.set_params(**best_record["params"])
    best_model.fit(feature_df[FEATURES], feature_df[TARGET_COL])

    leaderboard = pd.DataFrame(
        [{"model_name": r["model_name"], "params": r["params"], **r["avg_metrics"]} for r in results]
    ).sort_values(["rmse", "mae"]).reset_index(drop=True)
    return best_model, {"selected_model": best_record, "all_results": results, "cv_strategy": "expanding_window", "target": TARGET_COL}, leaderboard
