"""Probability calibration diagnostics."""
from __future__ import annotations
from typing import Dict
import numpy as np


def brier_score(y_true, y_prob) -> float:
    y = np.asarray(y_true, dtype=float)
    p = np.clip(np.asarray(y_prob, dtype=float), 0.0, 1.0)
    return float(np.mean((p - y) ** 2))


def expected_calibration_error(y_true, y_prob, n_bins: int = 10) -> float:
    y = np.asarray(y_true, dtype=float)
    p = np.clip(np.asarray(y_prob, dtype=float), 0.0, 1.0)
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        right_closed = i == n_bins - 1
        mask = (p >= edges[i]) & ((p <= edges[i + 1]) if right_closed else (p < edges[i + 1]))
        if np.any(mask):
            ece += float(np.mean(mask)) * abs(float(np.mean(y[mask])) - float(np.mean(p[mask])))
    return float(ece)


def reliability_table(y_true, y_prob, n_bins: int = 10) -> Dict[str, list]:
    y = np.asarray(y_true, dtype=float)
    p = np.clip(np.asarray(y_prob, dtype=float), 0.0, 1.0)
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    out = {"bin_lower": [], "bin_upper": [], "count": [], "mean_probability": [], "event_rate": []}
    for i in range(n_bins):
        mask = (p >= edges[i]) & ((p <= edges[i + 1]) if i == n_bins - 1 else (p < edges[i + 1]))
        if np.any(mask):
            out["bin_lower"].append(float(edges[i])); out["bin_upper"].append(float(edges[i+1]))
            out["count"].append(int(mask.sum())); out["mean_probability"].append(float(p[mask].mean()))
            out["event_rate"].append(float(y[mask].mean()))
    return out
