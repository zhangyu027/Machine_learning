from pathlib import Path
import pandas as pd

REQUIRED=["event_id","event_month","county","program","site_id","risk_score","service_count","prior_utilization","social_need_index"]
NUMERIC=["risk_score","service_count","prior_utilization","social_need_index"]

def bronze_ingest(raw_path,bronze_path):
    df=pd.read_csv(raw_path)
    missing=sorted(set(REQUIRED)-set(df.columns))
    if missing: raise ValueError(f"Missing required columns: {missing}")
    p=Path(bronze_path);p.parent.mkdir(parents=True,exist_ok=True);df.to_parquet(p,index=False)
    return df

def silver_clean(bronze_path,silver_path):
    df=pd.read_parquet(bronze_path)
    df["event_month"]=pd.to_datetime(df.event_month,errors="coerce")
    for c in NUMERIC: df[c]=pd.to_numeric(df[c],errors="coerce")
    df=df.dropna(subset=REQUIRED).drop_duplicates(subset=["event_id"])
    df=df[df.risk_score.between(0,1)&df.social_need_index.between(0,1)&(df.service_count>=0)].copy()
    df["year"]=df.event_month.dt.year;df["month"]=df.event_month.dt.month
    p=Path(silver_path);p.parent.mkdir(parents=True,exist_ok=True);df.to_parquet(p,index=False)
    return df

def gold_certified_tables(silver_path,gold_path,csv_path):
    df=pd.read_parquet(silver_path)
    gold=(df.groupby(["event_month","county","program"],as_index=False)
          .agg(total_services=("service_count","sum"),avg_risk_score=("risk_score","mean"),
               avg_social_need=("social_need_index","mean"),
               total_prior_utilization=("prior_utilization","sum"),
               actual_monthly_demand=("event_id","count"),record_count=("event_id","count"))
          .sort_values(["county","program","event_month"]))
    gold["target_next_month_demand"]=gold.groupby(["county","program"]).actual_monthly_demand.shift(-1)
    gp=Path(gold_path);cp=Path(csv_path);gp.parent.mkdir(parents=True,exist_ok=True);cp.parent.mkdir(parents=True,exist_ok=True)
    gold.to_parquet(gp,index=False);gold.to_csv(cp,index=False)
    return gold
