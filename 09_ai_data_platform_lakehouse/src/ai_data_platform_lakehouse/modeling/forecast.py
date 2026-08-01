from pathlib import Path
import json, joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
FEATURE_COLS=["total_services_lag1","total_services_rolling3","avg_risk_score_lag1","avg_risk_score_rolling3","avg_social_need_lag1","avg_social_need_rolling3","total_prior_utilization_lag1","total_prior_utilization_rolling3","record_count"]

def chronological_split(df: pd.DataFrame, test_fraction: float=.25):
    if not 0<test_fraction<1: raise ValueError("test_fraction must be between 0 and 1")
    ordered=df.sort_values("event_month").reset_index(drop=True); split=max(1,int(len(ordered)*(1-test_fraction))); return ordered.iloc[:split],ordered.iloc[split:]

def train_forecasting_model(feature_path: str | Path, model_path: str | Path, metrics_path: str | Path, predictions_path: str | Path, test_fraction: float=.25) -> dict:
    df=pd.read_parquet(feature_path); train,test=chronological_split(df,test_fraction)
    if test.empty: raise ValueError("Not enough rows for chronological test split")
    model=RandomForestRegressor(n_estimators=250,random_state=42,min_samples_leaf=2,n_jobs=-1); model.fit(train[FEATURE_COLS],train.target_next_month_demand); pred=model.predict(test[FEATURE_COLS])
    metrics={"mae":float(mean_absolute_error(test.target_next_month_demand,pred)),"rmse":float(mean_squared_error(test.target_next_month_demand,pred)**.5),"r2":float(r2_score(test.target_next_month_demand,pred)),"n_train":int(len(train)),"n_test":int(len(test)),"train_end":str(pd.to_datetime(train.event_month).max().date()),"test_start":str(pd.to_datetime(test.event_month).min().date()),"model_type":"RandomForestRegressor","validation":"chronological_holdout"}
    mp=Path(model_path); jp=Path(metrics_path); pp=Path(predictions_path); mp.parent.mkdir(parents=True,exist_ok=True); jp.parent.mkdir(parents=True,exist_ok=True); pp.parent.mkdir(parents=True,exist_ok=True); joblib.dump(model,mp); jp.write_text(json.dumps(metrics,indent=2),encoding='utf-8')
    out=test[["event_month","county","program",*FEATURE_COLS]].copy(); out["actual_demand"]=test.target_next_month_demand.values; out["predicted_demand"]=pred; out.to_csv(pp,index=False); return metrics
