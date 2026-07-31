"""Beta-Binomial Bayesian A/B testing."""
from __future__ import annotations

import numpy as np


def beta_binomial_ab_test(
    success_t: int,
    n_t: int,
    success_c: int,
    n_c: int,
    prior_alpha: float = 1.0,
    prior_beta: float = 1.0,
    draws: int = 100_000,
    seed: int = 42,
) -> dict[str, float | list[float] | int]:
    """Compare treatment and control conversion rates using posterior simulation."""
    if not (0 <= success_t <= n_t and 0 <= success_c <= n_c):
        raise ValueError("Success counts must be between zero and the corresponding sample size")
    if n_t <= 0 or n_c <= 0 or draws <= 0:
        raise ValueError("Sample sizes and draws must be positive")
    if prior_alpha <= 0 or prior_beta <= 0:
        raise ValueError("Prior parameters must be positive")

    rng = np.random.default_rng(seed)
    treatment = rng.beta(prior_alpha + success_t, prior_beta + n_t - success_t, draws)
    control = rng.beta(prior_alpha + success_c, prior_beta + n_c - success_c, draws)
    lift = treatment - control
    return {
        "prob_treatment_better": float((lift > 0).mean()),
        "expected_lift": float(lift.mean()),
        "credible_interval_95": [
            float(np.quantile(lift, 0.025)),
            float(np.quantile(lift, 0.975)),
        ],
        "expected_loss_if_ship": float(np.maximum(-lift, 0).mean()),
        "expected_loss_if_do_not_ship": float(np.maximum(lift, 0).mean()),
        "draws": int(draws),
    }
