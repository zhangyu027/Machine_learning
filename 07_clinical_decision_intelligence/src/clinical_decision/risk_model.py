from __future__ import annotations
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.model_selection import train_test_split
from clinical_decision.features import FEATURE_COLUMNS


def _make_model():
    try:
        from xgboost import XGBClassifier
        return XGBClassifier(n_estimators=150, max_depth=4, learning_rate=0.05, subsample=0.85, eval_metric="logloss", random_state=42)
    except Exception:
        return GradientBoostingClassifier(random_state=42)


def train_risk_model(df: pd.DataFrame, target: str = "readmission_30d") -> dict:
    X = df[FEATURE_COLUMNS]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, random_state=42, stratify=y)
    model = _make_model()
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    return {
        "model": model,
        "roc_auc": float(roc_auc_score(y_test, prob)),
        "avg_precision": float(average_precision_score(y_test, prob)),
        "features": FEATURE_COLUMNS,
    }
