import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score

FEATURES = ["age","sex","insurance","hospital_id","comorbidity_index","prior_admissions_12m",
            "severity_score","care_management_program","length_of_stay"]

def train_xgboost_readmission(df: pd.DataFrame, target="readmitted_30d"):
    X = pd.get_dummies(df[FEATURES], drop_first=True)
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, random_state=42, stratify=y)
    model = XGBClassifier(n_estimators=220, max_depth=4, learning_rate=.05, subsample=.85,
                          colsample_bytree=.85, eval_metric="logloss", random_state=42)
    model.fit(X_train, y_train)
    pred = model.predict_proba(X_test)[:, 1]
    metrics = {"roc_auc": float(roc_auc_score(y_test, pred)), "average_precision": float(average_precision_score(y_test, pred))}
    return model, list(X.columns), metrics

def save_model(model, feature_columns, path):
    joblib.dump({"model": model, "feature_columns": feature_columns}, path)
