from __future__ import annotations
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from clinical_decision.features import FEATURE_COLUMNS


def estimate_heterogeneous_treatment_effects(df: pd.DataFrame, outcome: str = "readmission_30d") -> pd.DataFrame:
    """Causal-forest-style T-learner fallback.

    In a production environment, this can be replaced with econml.CausalForestDML.
    The API intentionally returns patient-level CATE estimates and segment summaries.
    """
    treated = df[df.treatment == 1]
    control = df[df.treatment == 0]
    control_model = RandomForestRegressor(n_estimators=200, min_samples_leaf=20, random_state=42)
    treatment_model = RandomForestRegressor(n_estimators=200, min_samples_leaf=20, random_state=42)
    control_model.fit(control[FEATURE_COLUMNS], control[outcome])
    treatment_model.fit(treated[FEATURE_COLUMNS], treated[outcome])
    out = df.copy()
    out["mu0"] = control_model.predict(out[FEATURE_COLUMNS])
    out["mu1"] = treatment_model.predict(out[FEATURE_COLUMNS])
    out["cate"] = out["mu1"] - out["mu0"]
    out["benefit_segment"] = pd.cut(out["cate"], bins=[-1, -0.05, 0.05, 1], labels=["benefit", "neutral", "harm_risk"])
    return out
