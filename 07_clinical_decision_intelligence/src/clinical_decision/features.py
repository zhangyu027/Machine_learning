from __future__ import annotations
import pandas as pd

FEATURE_COLUMNS = [
    "age", "comorbidity_score", "baseline_risk_score", "prior_visits", "lab_abnormality_score", "is_female"
]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["is_female"] = (out["sex"].str.lower() == "female").astype(int)
    out["risk_age_interaction"] = out["age"] * out["baseline_risk_score"]
    return out
