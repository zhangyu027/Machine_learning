from __future__ import annotations
import joblib
import pandas as pd
from src.ml.train_xgboost_readmission import FEATURES

class ReadmissionPredictor:
    def __init__(self, model_path):
        bundle = joblib.load(model_path)
        self.model = bundle["model"]
        self.feature_columns = bundle["feature_columns"]

    def transform(self, records: list[dict]) -> pd.DataFrame:
        frame = pd.DataFrame(records)
        missing = [c for c in FEATURES if c not in frame.columns]
        if missing:
            raise ValueError(f"Missing required features: {missing}")
        encoded = pd.get_dummies(frame[FEATURES], drop_first=True)
        return encoded.reindex(columns=self.feature_columns, fill_value=0)

    def predict(self, records: list[dict]) -> list[float]:
        x = self.transform(records)
        return self.model.predict_proba(x)[:, 1].astype(float).tolist()
