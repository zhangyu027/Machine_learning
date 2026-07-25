"""Shared endpoint metrics for classification and regression ADMET tasks."""
from __future__ import annotations
from typing import Dict
from sklearn.metrics import roc_auc_score, average_precision_score, mean_absolute_error, mean_squared_error
from .calibration import brier_score, expected_calibration_error


def classification_report(y_true, y_prob) -> Dict[str, float]:
    return {"roc_auc": float(roc_auc_score(y_true, y_prob)), "pr_auc": float(average_precision_score(y_true, y_prob)), "brier": brier_score(y_true, y_prob), "ece": expected_calibration_error(y_true, y_prob)}


def regression_report(y_true, y_pred) -> Dict[str, float]:
    return {"mae": float(mean_absolute_error(y_true, y_pred)), "rmse": float(mean_squared_error(y_true, y_pred) ** 0.5)}
