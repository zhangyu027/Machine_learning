from pathlib import Path
import numpy as np
import pandas as pd


def generate_synthetic_public_health_events(
    n_records=10000,
    output_path="data/raw/public_health_events.csv",
    seed=42,
):
    rng = np.random.default_rng(seed)

    months = pd.date_range("2025-01-01", periods=18, freq="MS")
    counties = ["Orange", "Los Angeles", "San Diego", "Riverside", "San Bernardino"]
    programs = ["Clinic_Access", "Preventive_Care", "Enrollment_Support", "Telehealth"]
    sites = [f"SITE_{i:03d}" for i in range(1, 61)]

    df = pd.DataFrame({
        "event_id": [f"EVT_{i:08d}" for i in range(n_records)],
        "event_month": rng.choice(months, n_records),
        "county": rng.choice(counties, n_records),
        "program": rng.choice(programs, n_records),
        "site_id": rng.choice(sites, n_records),
        "age_band": rng.choice(["0-17", "18-34", "35-54", "55+"], n_records, p=[0.18, 0.28, 0.32, 0.22]),
        "risk_score": rng.beta(2.2, 4.8, n_records),
        "service_count": rng.poisson(2.2, n_records) + 1,
        "prior_utilization": rng.poisson(1.8, n_records),
        "social_need_index": rng.normal(0.45, 0.18, n_records).clip(0, 1),
    })

    df["target_next_month_demand"] = (
        10
        + 2.5 * df["service_count"]
        + 8.0 * df["risk_score"]
        + 3.0 * df["prior_utilization"]
        + 12.0 * df["social_need_index"]
        + rng.normal(0, 4, n_records)
    ).clip(0)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    df = generate_synthetic_public_health_events()
    print(df.shape)
