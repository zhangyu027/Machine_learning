import numpy as np
import pandas as pd

def simulate_thompson_sampling(true_rates, steps=5000, seed=42):
    rng = np.random.default_rng(seed)
    k = len(true_rates)
    alpha = np.ones(k)
    beta = np.ones(k)
    rows = []
    for step in range(1, steps + 1):
        sampled = rng.beta(alpha, beta)
        arm = int(np.argmax(sampled))
        reward = rng.binomial(1, true_rates[arm])
        alpha[arm] += reward
        beta[arm] += 1 - reward
        if step % 100 == 0:
            rows.append({"step": step, **{f"posterior_mean_arm_{i}": alpha[i] / (alpha[i] + beta[i]) for i in range(k)}})
    return pd.DataFrame(rows)
