from pathlib import Path
import json, joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
FEATURE_COLS=["total_services_lag1","total_services_rolling3","avg_risk_score_lag1","avg_risk_score_rolling3","avg_social_need_lag1","avg_social_need_rolling3","total_prior_utilization_lag1","total_prior_utilization_rolling3","record_count_lag1"]

def chronological_split(df: pd.DataFrame, test_fraction: float=.25):
    if not 0<test_fraction<1: raise ValueError("test_fraction must be between 0 and 1")
    ordered=df.sort_values("event_month").reset_index(drop=True)
    months=sorted(pd.to_datetime(ordered.event_month).unique())
    if len(months)<4: raise ValueError("At least four months required")
    split=max(1,int(len(months)*(1-test_fraction)))
    cutoff=months[split]
    train=ordered[pd.to_datetime(ordered.event_month)<cutoff]
    test=ordered[pd.to_datetime(ordered.event_month)>=cutoff]
    assert train.event_month.max()<test.event_month.min()
    return train,test

def train_forecasting_model(feature_path: str | Path, model_path: str | Path, metrics_path: str | Path, predictions_path: str | Path, test_fraction: float=.25) -> dict:
    df=pd.read_parquet(feature_path); train,test=chronological_split(df,test_fraction)
    if test.empty: raise ValueError("Not enough rows for chronological test split")
    model=RandomForestRegressor(n_estimators=250,random_state=42,min_samples_leaf=2,n_jobs=-1); model.fit(train[FEATURE_COLS],train.target_next_month_demand); pred=model.predict(test[FEATURE_COLS])
    # A leakage-safe, training-only group mean benchmark (global fallback).
    group_means=train.groupby(["county","program"]).target_next_month_demand.mean()
    global_mean=float(train.target_next_month_demand.mean())
    baseline=pd.Series([group_means.get((r.county,r.program),global_mean) for r in test.itertuples()],index=test.index)
    baseline_mae=float(mean_absolute_error(test.target_next_month_demand,baseline))
    metrics={"baseline_mae":baseline_mae,"baseline_name":"train_group_mean","wape":float(abs(test.target_next_month_demand-pred).sum()/abs(test.target_next_month_demand).sum()),"bias":float((pred-test.target_next_month_demand).mean()),"mae":float(mean_absolute_error(test.target_next_month_demand,pred)),"rmse":float(mean_squared_error(test.target_next_month_demand,pred)**.5),"r2":float(r2_score(test.target_next_month_demand,pred)),"n_train":int(len(train)),"n_test":int(len(test)),"train_end":str(pd.to_datetime(train.event_month).max().date()),"test_start":str(pd.to_datetime(test.event_month).min().date()),"model_type":"RandomForestRegressor","validation":"chronological_holdout"}
    mp=Path(model_path); jp=Path(metrics_path); pp=Path(predictions_path); mp.parent.mkdir(parents=True,exist_ok=True); jp.parent.mkdir(parents=True,exist_ok=True); pp.parent.mkdir(parents=True,exist_ok=True); joblib.dump(model,mp); jp.write_text(json.dumps(metrics,indent=2),encoding='utf-8')
    out=test[["event_month","county","program",*FEATURE_COLS]].copy(); out["actual_demand"]=test.target_next_month_demand.values; out["predicted_demand"]=pred; out.to_csv(pp,index=False); return metrics
