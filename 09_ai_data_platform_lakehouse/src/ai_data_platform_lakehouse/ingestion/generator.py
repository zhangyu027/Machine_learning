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
    df["target_next_month_demand"]=(10+2.5*df.service_count+8*df.risk_score+3*df.prior_utilization+12*df.social_need_index+rng.normal(0,4,n_records)).clip(0)
    p=Path(output_path); p.parent.mkdir(parents=True,exist_ok=True); df.to_csv(p,index=False); return df
