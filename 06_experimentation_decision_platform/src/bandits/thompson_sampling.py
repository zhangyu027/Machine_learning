"""Thompson Sampling simulation for Bernoulli rewards."""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd


def simulate_thompson_sampling(
    true_rates: Sequence[float], steps: int = 5_000, seed: int = 42, snapshot_every: int = 100
) -> pd.DataFrame:
    """Simulate posterior learning and adaptive arm selection."""
    rates = np.asarray(true_rates, dtype=float)
    if rates.size < 2 or np.any((rates < 0) | (rates > 1)):
        raise ValueError("Provide at least two true rates between zero and one")
    if steps <= 0 or snapshot_every <= 0:
        raise ValueError("Steps and snapshot frequency must be positive")
    rng = np.random.default_rng(seed)
    alpha = np.ones(rates.size)
    beta = np.ones(rates.size)
    pulls = np.zeros(rates.size, dtype=int)
    rows: list[dict[str, float | int]] = []
    for step in range(1, steps + 1):
        arm = int(np.argmax(rng.beta(alpha, beta)))
        reward = int(rng.binomial(1, rates[arm]))
        pulls[arm] += 1
        alpha[arm] += reward
        beta[arm] += 1 - reward
        if step % snapshot_every == 0 or step == steps:
            row: dict[str, float | int] = {"step": step, "selected_arm": arm}
            for index in range(rates.size):
                row[f"posterior_mean_arm_{index}"] = float(alpha[index] / (alpha[index] + beta[index]))
                row[f"pulls_arm_{index}"] = int(pulls[index])
            rows.append(row)
    return pd.DataFrame(rows)
