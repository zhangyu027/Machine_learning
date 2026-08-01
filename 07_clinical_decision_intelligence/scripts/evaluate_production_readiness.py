import json, joblib
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from clinical_decision_intelligence.ml.train_xgboost_readmission import FEATURES
from clinical_decision_intelligence.evaluation.calibration import calibration_report
from clinical_decision_intelligence.evaluation.fairness import subgroup_fairness_report
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/raw/patient_encounters.csv')
bundle=joblib.load(ROOT/'models/xgboost_readmission_model.joblib')
X=pd.get_dummies(df[FEATURES],drop_first=True).reindex(columns=bundle['feature_columns'],fill_value=0)
p=bundle['model'].predict_proba(X)[:,1]
eval_df=df.copy(); eval_df['predicted_readmission_risk']=p
reports={
 'calibration':calibration_report(df['readmitted_30d'],p),
 'fairness_by_sex':subgroup_fairness_report(eval_df,'readmitted_30d','predicted_readmission_risk','sex'),
 'fairness_by_insurance':subgroup_fairness_report(eval_df,'readmitted_30d','predicted_readmission_risk','insurance')}
out=ROOT/'reports/model_outputs/production_evaluation.json'; out.write_text(json.dumps(reports,indent=2)); print(out)
