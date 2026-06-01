from __future__ import annotations
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
from clinical_decision.features import FEATURE_COLUMNS


def estimate_propensity_scores(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    model = LogisticRegression(max_iter=1000)
    model.fit(out[FEATURE_COLUMNS], out["treatment"])
    out["propensity_score"] = model.predict_proba(out[FEATURE_COLUMNS])[:, 1]
    return out


def propensity_match(df: pd.DataFrame, caliper: float = 0.05) -> pd.DataFrame:
    treated = df[df.treatment == 1].copy()
    control = df[df.treatment == 0].copy()
    nn = NearestNeighbors(n_neighbors=1)
    nn.fit(control[["propensity_score"]])
    dist, idx = nn.kneighbors(treated[["propensity_score"]])
    matched_control = control.iloc[idx.flatten()].copy().reset_index(drop=True)
    treated = treated.reset_index(drop=True)
    pairs = pd.concat([
        treated.add_prefix("treated_"),
        matched_control.add_prefix("control_")
    ], axis=1)
    pairs["abs_ps_distance"] = dist.flatten()
    return pairs[pairs["abs_ps_distance"] <= caliper]


def average_treatment_effect_on_treated(matched_pairs: pd.DataFrame, outcome_col: str = "readmission_30d") -> float:
    return float((matched_pairs[f"treated_{outcome_col}"] - matched_pairs[f"control_{outcome_col}"]).mean())
