from pathlib import Path
import pandas as pd
BASE=["total_services","avg_risk_score","avg_social_need","total_prior_utilization"]
def build_feature_store(gold_path: str | Path, feature_path: str | Path, csv_path: str | Path) -> pd.DataFrame:
    df=pd.read_parquet(gold_path); df["event_month"]=pd.to_datetime(df.event_month); df=df.sort_values(["county","program","event_month"]).copy()
    groups=df.groupby(["county","program"],sort=False)
    for c in BASE:
        df[f"{c}_lag1"]=groups[c].shift(1)
        df[f"{c}_rolling3"]=groups[c].transform(lambda s:s.shift(1).rolling(3,min_periods=1).mean())
    df=df.dropna().reset_index(drop=True)
    p=Path(feature_path); cp=Path(csv_path); p.parent.mkdir(parents=True,exist_ok=True); cp.parent.mkdir(parents=True,exist_ok=True); df.to_parquet(p,index=False); df.to_csv(cp,index=False); return df
