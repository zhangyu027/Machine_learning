"""T-Learner for heterogeneous treatment-effect estimation."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


class TLearnerUpliftModel:
    """Fit separate outcome models for treatment and control groups."""

    def __init__(self, random_state: int = 42, n_estimators: int = 120) -> None:
        self.treatment_model = RandomForestRegressor(
            n_estimators=n_estimators, max_depth=9, random_state=random_state, n_jobs=-1
        )
        self.control_model = RandomForestRegressor(
            n_estimators=n_estimators, max_depth=9, random_state=random_state + 1, n_jobs=-1
        )
        self.feature_columns: list[str] | None = None

    def fit(self, X: pd.DataFrame, y: pd.Series, treatment: pd.Series) -> "TLearnerUpliftModel":
        if not ({0, 1} <= set(treatment.unique())):
            raise ValueError("Treatment indicator must contain both control (0) and treatment (1)")
        self.feature_columns = list(X.columns)
        self.treatment_model.fit(X.loc[treatment == 1], y.loc[treatment == 1])
        self.control_model.fit(X.loc[treatment == 0], y.loc[treatment == 0])
        return self

    def predict_cate(self, X: pd.DataFrame) -> np.ndarray:
        if self.feature_columns is None:
            raise RuntimeError("Model must be fitted before prediction")
        missing = set(self.feature_columns) - set(X.columns)
        if missing:
            raise ValueError(f"Missing model features: {sorted(missing)}")
        features = X[self.feature_columns]
        return self.treatment_model.predict(features) - self.control_model.predict(features)
