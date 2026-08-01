import pandas as pd
from sklearn.ensemble import RandomForestRegressor

class CausalForestStyleTLearner:
    def __init__(self, random_state=42):
        self.treated_model = RandomForestRegressor(n_estimators=150, max_depth=8, random_state=random_state, n_jobs=-1)
        self.control_model = RandomForestRegressor(n_estimators=150, max_depth=8, random_state=random_state + 1, n_jobs=-1)
        self.feature_columns = None

    def fit(self, X: pd.DataFrame, y: pd.Series, treatment: pd.Series):
        self.feature_columns = list(X.columns)
        self.treated_model.fit(X[treatment == 1], y[treatment == 1])
        self.control_model.fit(X[treatment == 0], y[treatment == 0])
        return self

    def predict_effect(self, X: pd.DataFrame):
        X = X[self.feature_columns]
        return self.treated_model.predict(X) - self.control_model.predict(X)
