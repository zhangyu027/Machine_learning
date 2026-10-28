from pathlib import Path
import numpy as np
import pandas as pd

def generate_synthetic_public_health_events(n_records: int = 10000, output_path: str | Path = "data/raw/public_health_events.csv", seed: int = 42) -> pd.DataFrame:
    if n_records <= 0: raise ValueError("n_records must be positive")
    rng=np.random.default_rng(seed)
    months=pd.date_range("2025-01-01",periods=18,freq="MS")
    counties=["Orange","Los Angeles","San Diego","Riverside","San Bernardino"]
    programs=["Clinic_Access","Preventive_Care","Enrollment_Support","Telehealth"]
    sites=[f"SITE_{i:03d}" for i in range(1,61)]
    df=pd.DataFrame({
      "event_id":[f"EVT_{i:08d}" for i in range(n_records)],
      "event_month":rng.choice(months,n_records),"county":rng.choice(counties,n_records),
      "program":rng.choice(programs,n_records),"site_id":rng.choice(sites,n_records),
      "age_band":rng.choice(["0-17","18-34","35-54","55+"],n_records,p=[.18,.28,.32,.22]),
      "risk_score":rng.beta(2.2,4.8,n_records),"service_count":rng.poisson(2.2,n_records)+1,
      "prior_utilization":rng.poisson(1.8,n_records),"social_need_index":rng.normal(.45,.18,n_records).clip(0,1)})
    # Persistent county/program-level variation plus annual seasonality creates a temporal signal.
    group_effect={(county,program):rng.uniform(0.75,1.25) for county in counties for program in programs}
    month_effect={month:1+0.12*np.sin(2*np.pi*(i%12)/12)+0.025*i/12 for i,month in enumerate(months)}
    factors=np.array([group_effect[(c,p)]*month_effect[pd.Timestamp(m)] for m,c,p in zip(df.event_month,df.county,df.program)])
    # Generate realized demand first; derive next-month labels by group and time.
    df["realized_demand"]=(10+2.5*df.service_count+8*df.risk_score+3*df.prior_utilization+12*df.social_need_index+rng.normal(0,4,n_records)).clip(0)*factors
    monthly=df.groupby(["event_month","county","program"])["realized_demand"].sum().rename("realized_monthly_demand").reset_index()
    monthly=monthly.sort_values(["county","program","event_month"])
    monthly["target_next_month_demand"]=monthly.groupby(["county","program"])["realized_monthly_demand"].shift(-1)
    counts=df.groupby(["event_month","county","program"]).size().rename("group_count").reset_index()
    df=df.merge(monthly[["event_month","county","program","target_next_month_demand"]],on=["event_month","county","program"],how="left")
    df=df.merge(counts,on=["event_month","county","program"],how="left")
    df["target_next_month_demand"]=df["target_next_month_demand"]/df["group_count"]
    df=df.drop(columns=["group_count"])
    df=df.drop(columns=["realized_demand"])
    df=df.dropna(subset=["target_next_month_demand"])
    p=Path(output_path); p.parent.mkdir(parents=True,exist_ok=True); df.to_csv(p,index=False); return df
