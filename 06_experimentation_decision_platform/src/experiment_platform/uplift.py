from __future__ import annotations
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

FEATURES = ["pre_period_metric", "age", "engagement_score"]


def train_t_learner(df: pd.DataFrame) -> dict:
    """Simple uplift model using two random forests: one control model and one treatment model."""
    work = df.copy()
    train, test = train_test_split(work, test_size=0.25, random_state=42)
    control_model = RandomForestRegressor(n_estimators=100, random_state=42, min_samples_leaf=10)
    treatment_model = RandomForestRegressor(n_estimators=100, random_state=42, min_samples_leaf=10)
    control_model.fit(train[train.variant == "control"][FEATURES], train[train.variant == "control"].post_period_metric)
    treatment_model.fit(train[train.variant == "treatment"][FEATURES], train[train.variant == "treatment"].post_period_metric)
    test = test.copy()
    test["pred_control"] = control_model.predict(test[FEATURES])
    test["pred_treatment"] = treatment_model.predict(test[FEATURES])
    test["estimated_uplift"] = test["pred_treatment"] - test["pred_control"]
    mae = mean_absolute_error(test.post_period_metric, test[["pred_control", "pred_treatment"]].mean(axis=1))
    return {"mae_proxy": float(mae), "top_uplift_segments": test.groupby("segment").estimated_uplift.mean().sort_values(ascending=False).to_dict()}
