import numpy as np

def beta_binomial_ab_test(success_t, n_t, success_c, n_c, prior_alpha=1, prior_beta=1, draws=100000, seed=42):
    rng = np.random.default_rng(seed)
    t = rng.beta(prior_alpha + success_t, prior_beta + n_t - success_t, draws)
    c = rng.beta(prior_alpha + success_c, prior_beta + n_c - success_c, draws)
    lift = t - c
    return {
        "prob_treatment_better": float((lift > 0).mean()),
        "expected_lift": float(lift.mean()),
        "credible_interval_95": [float(np.quantile(lift, 0.025)), float(np.quantile(lift, 0.975))],
        "expected_loss_if_ship": float(np.maximum(-lift, 0).mean()),
        "expected_loss_if_do_not_ship": float(np.maximum(lift, 0).mean()),
    }
