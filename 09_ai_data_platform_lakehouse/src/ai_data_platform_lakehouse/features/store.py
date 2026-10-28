from pathlib import Path
import numpy as np
import pandas as pd

def build_feature_store(gold_path,feature_path,csv_path):
    df=pd.read_parquet(gold_path)
    df["event_month"]=pd.to_datetime(df.event_month)
    df=df.sort_values(["county","program","event_month"]).copy()
    groups=df.groupby(["county","program"],sort=False)
    # End-of-month t forecast for month t+1: t demand is observed and available.
    df["demand_t"]=df.actual_monthly_demand
    df["demand_lag1"]=groups.actual_monthly_demand.shift(1)
    df["demand_lag2"]=groups.actual_monthly_demand.shift(2)
    df["demand_rolling3"]=groups.actual_monthly_demand.transform(lambda x:x.rolling(3,min_periods=3).mean())
    df["forecast_month"]=(df.event_month+pd.offsets.MonthBegin(1))
    df["month_sin"]=np.sin(2*np.pi*df.forecast_month.dt.month/12)
    df["month_cos"]=np.cos(2*np.pi*df.forecast_month.dt.month/12)
    df=df.dropna(subset=["target_next_month_demand","demand_lag1","demand_lag2","demand_rolling3"]).reset_index(drop=True)
    p=Path(feature_path);c=Path(csv_path);p.parent.mkdir(parents=True,exist_ok=True);c.parent.mkdir(parents=True,exist_ok=True)
    df.to_parquet(p,index=False);df.to_csv(c,index=False)
    return df
