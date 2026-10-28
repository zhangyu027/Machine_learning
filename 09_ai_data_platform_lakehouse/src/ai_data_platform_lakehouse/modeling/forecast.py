from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

FEATURE_COLS=["demand_t","demand_lag1","demand_lag2","demand_rolling3","month_sin","month_cos"]
def chronological_split(df,test_fraction=.25):
    if not 0<test_fraction<1: raise ValueError("test_fraction must be between 0 and 1")
    ordered=df.sort_values("event_month").reset_index(drop=True)
    months=sorted(pd.to_datetime(ordered.event_month).unique())
    if len(months)<4: raise ValueError("At least four months required")
    cutoff=months[max(1,int(len(months)*(1-test_fraction)))]
    train=ordered[ordered.event_month<cutoff];test=ordered[ordered.event_month>=cutoff]
    assert train.event_month.max()<test.event_month.min()
    return train,test

def evaluate(actual,pred):
    actual=np.asarray(actual);pred=np.asarray(pred)
    return {"mae":float(mean_absolute_error(actual,pred)),
            "rmse":float(np.sqrt(mean_squared_error(actual,pred))),
            "r2":float(r2_score(actual,pred)),
            "wape":float(np.abs(actual-pred).sum()/max(np.abs(actual).sum(),1e-9)),
            "bias":float(np.mean(pred-actual))}

def train_forecasting_model(feature_path,model_path,metrics_path,predictions_path,test_fraction=.25):
    df=pd.read_parquet(feature_path);df.event_month=pd.to_datetime(df.event_month)
    train,test=chronological_split(df,test_fraction)
    model=RandomForestRegressor(n_estimators=250,random_state=42,min_samples_leaf=2,n_jobs=-1)
    model.fit(train[FEATURE_COLS],train.target_next_month_demand)
    pred=model.predict(test[FEATURE_COLS])
    baseline=test.demand_t.to_numpy()
    metrics=evaluate(test.target_next_month_demand,pred)
    metrics.update({"baseline_name":"last_observed_month","baseline_mae":float(mean_absolute_error(test.target_next_month_demand,baseline)),
                    "n_train":len(train),"n_test":len(test),"train_end":str(train.event_month.max().date()),
                    "test_start":str(test.event_month.min().date()),"model_type":"RandomForestRegressor","validation":"chronological_holdout"})
    # Expanding-window one-step backtests; each fold uses only months earlier than its test month.
    months=sorted(df.event_month.unique());folds=[]
    for month in months[max(12,len(months)//2):]:
        tr=df[df.event_month<month];te=df[df.event_month==month]
        if tr.empty or te.empty:continue
        m=RandomForestRegressor(n_estimators=100,random_state=42,min_samples_leaf=2,n_jobs=-1)
        m.fit(tr[FEATURE_COLS],tr.target_next_month_demand)
        folds.append({"test_month":str(pd.Timestamp(month).date()),
                      "model_mae":float(mean_absolute_error(te.target_next_month_demand,m.predict(te[FEATURE_COLS]))),
                      "baseline_mae":float(mean_absolute_error(te.target_next_month_demand,te.demand_t))})
    metrics["backtest_folds"]=folds
    mp=Path(model_path);jp=Path(metrics_path);pp=Path(predictions_path)
    for p in [mp,jp,pp]:p.parent.mkdir(parents=True,exist_ok=True)
    joblib.dump(model,mp);jp.write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    out=test[["event_month","forecast_month","county","program",*FEATURE_COLS]].copy()
    out["actual_demand"]=test.target_next_month_demand.values
    out["predicted_demand"]=pred
    out["baseline_prediction"]=baseline
    out.to_csv(pp,index=False)
    return metrics
