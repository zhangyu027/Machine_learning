from pathlib import Path
import numpy as np
import pandas as pd

COUNTIES=["Orange","Los Angeles","San Diego","Riverside","San Bernardino"]
PROGRAMS=["Clinic_Access","Preventive_Care","Enrollment_Support","Telehealth"]

def generate_synthetic_public_health_events(n_records=10000,output_path="data/raw/public_health_events.csv",seed=42):
    if n_records<=0: raise ValueError("n_records must be positive")
    rng=np.random.default_rng(seed)
    months=pd.date_range("2022-01-01",periods=60,freq="MS")
    groups=[(c,p) for c in COUNTIES for p in PROGRAMS]
    # Simulate a persistent monthly demand process, then sample events within each group-month.
    base={g:rng.uniform(22,40) for g in groups}
    previous={g:base[g] for g in groups}
    cells=[]
    for i,month in enumerate(months):
        for g in groups:
            seasonal=1+0.12*np.sin(2*np.pi*(i%12)/12)
            expected=0.72*previous[g]+0.28*base[g]*seasonal
            demand=max(5,int(round(expected+rng.normal(0,2))))
            previous[g]=demand
            cells.append((month,g[0],g[1],demand))
    demand=pd.DataFrame(cells,columns=["event_month","county","program","actual_monthly_demand"])
    # Each event represents one realized demand unit, so monthly counts are the observed target.
    rows=[]
    for month,county,program,count in demand.itertuples(index=False,name=None):
        for _ in range(count):
            rows.append((month,county,program))
    df=pd.DataFrame(rows,columns=["event_month","county","program"])
    df["event_id"]=[f"EVT_{i:08d}" for i in range(len(df))]
    df["site_id"]=rng.choice([f"SITE_{i:03d}" for i in range(1,61)],len(df))
    df["age_band"]=rng.choice(["0-17","18-34","35-54","55+"],len(df))
    df["risk_score"]=rng.beta(2.2,4.8,len(df))
    df["service_count"]=rng.poisson(2.2,len(df))+1
    df["prior_utilization"]=rng.poisson(1.8,len(df))
    df["social_need_index"]=rng.normal(.45,.18,len(df)).clip(0,1)
    path=Path(output_path);path.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(path,index=False)
    return df
