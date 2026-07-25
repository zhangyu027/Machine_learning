"""Bootstrap confidence intervals for molecular model metrics."""
from __future__ import annotations
from typing import Callable, Tuple
import numpy as np


def bootstrap_confidence_interval(
    y_true,
    y_score,
    metric: Callable,
    n_bootstrap: int = 500,
    confidence: float = 0.95,
    random_state: int = 42,
) -> Tuple[float, float]:
    y = np.asarray(y_true)
    s = np.asarray(y_score)
    if len(y) != len(s) or len(y) == 0:
        raise ValueError("y_true and y_score must have equal non-zero length")
    rng = np.random.default_rng(random_state)
    estimates = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, len(y), len(y))
        try:
            estimates.append(float(metric(y[idx], s[idx])))
        except ValueError:
            continue
    if not estimates:
        return float("nan"), float("nan")
    alpha = 1.0 - confidence
    return (float(np.quantile(estimates, alpha / 2)), float(np.quantile(estimates, 1 - alpha / 2)))
