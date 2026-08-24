from pathlib import Path
import json, pandas as pd, mlflow, mlflow.sklearn
from clinical_decision_intelligence.core.config import MLFLOW_TRACKING_URI
from clinical_decision_intelligence.ml.train_xgboost_readmission import train_xgboost_readmission
ROOT=Path(__file__).resolve().parents[1]
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI); mlflow.set_experiment("clinical-decision-intelligence")
df=pd.read_csv(ROOT/'data/raw/patient_encounters.csv')
with mlflow.start_run():
    model, columns, metrics=train_xgboost_readmission(df)
    mlflow.log_metrics(metrics); mlflow.log_dict({"feature_columns":columns},"feature_schema.json")
    mlflow.sklearn.log_model(model,"model",registered_model_name="readmission-risk-xgboost")
    print(json.dumps(metrics,indent=2))
