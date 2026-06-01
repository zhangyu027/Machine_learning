import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def doubly_robust_ate(X: pd.DataFrame, y: pd.Series, treatment: pd.Series, propensity_scores: pd.Series):
    mu1 = RandomForestRegressor(n_estimators=150, max_depth=8, random_state=3, n_jobs=-1)
    mu0 = RandomForestRegressor(n_estimators=150, max_depth=8, random_state=4, n_jobs=-1)
    mu1.fit(X[treatment == 1], y[treatment == 1])
    mu0.fit(X[treatment == 0], y[treatment == 0])
    m1 = mu1.predict(X)
    m0 = mu0.predict(X)
    p = np.clip(propensity_scores.to_numpy(), 1e-3, 1 - 1e-3)
    t = treatment.to_numpy()
    yy = y.to_numpy()
    dr = (m1 - m0) + t * (yy - m1) / p - (1 - t) * (yy - m0) / (1 - p)
    return {"ate": float(np.mean(dr)), "treated_model": mu1, "control_model": mu0}
