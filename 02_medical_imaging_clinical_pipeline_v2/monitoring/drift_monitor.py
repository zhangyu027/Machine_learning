"""Simple input and prediction drift checks using Population Stability Index (PSI)."""
from __future__ import annotations

import numpy as np


def population_stability_index(reference, current, bins=10, epsilon=1e-6):
    reference = np.asarray(reference, dtype=float)
    current = np.asarray(current, dtype=float)
    edges = np.unique(np.quantile(reference, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:
        return 0.0
    ref_counts, _ = np.histogram(reference, bins=edges)
    cur_counts, _ = np.histogram(current, bins=edges)
    ref_pct = np.clip(ref_counts / max(ref_counts.sum(), 1), epsilon, None)
    cur_pct = np.clip(cur_counts / max(cur_counts.sum(), 1), epsilon, None)
    return float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))


def classify_drift(psi):
    if psi < 0.1:
        return "stable"
    if psi < 0.25:
        return "review"
    return "significant_drift"
