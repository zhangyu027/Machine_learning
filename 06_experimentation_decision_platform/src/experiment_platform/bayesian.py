from __future__ import annotations
import numpy as np
import pandas as pd


def beta_binomial_ab(df: pd.DataFrame, draws: int = 20000, seed: int = 42) -> dict:
    """Bayesian conversion comparison using Beta(1,1) priors."""
    rng = np.random.default_rng(seed)
    c = df[df.variant == "control"].converted.astype(int)
    t = df[df.variant == "treatment"].converted.astype(int)
    control_post = rng.beta(1 + c.sum(), 1 + len(c) - c.sum(), draws)
    treatment_post = rng.beta(1 + t.sum(), 1 + len(t) - t.sum(), draws)
    lift = treatment_post - control_post
    return {
        "prob_treatment_better": float((lift > 0).mean()),
        "expected_lift": float(lift.mean()),
        "credible_interval_95": [float(np.quantile(lift, .025)), float(np.quantile(lift, .975))],
    }
