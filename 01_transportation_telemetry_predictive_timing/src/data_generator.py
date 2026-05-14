from pathlib import Path
import numpy as np
import pandas as pd


def generate_synthetic_telemetry(n_events=5000, output_path="data/raw/train_telemetry_events.csv", seed=42):
    rng = np.random.default_rng(seed)

    train_ids = [f"TRAIN_{i:04d}" for i in range(1, 201)]
    route_ids = [f"ROUTE_{i:03d}" for i in range(1, 31)]

    start = pd.Timestamp("2026-01-01 00:00:00")
    event_offsets = rng.integers(0, 60 * 24 * 30, size=n_events)
    event_times = [start + pd.Timedelta(minutes=int(x)) for x in event_offsets]

    scheduled_minutes = rng.normal(180, 45, n_events).clip(40, 420)
    distance_miles = rng.normal(220, 80, n_events).clip(20, 600)
    avg_speed_mph = (distance_miles / (scheduled_minutes / 60)) + rng.normal(0, 8, n_events)
    avg_speed_mph = avg_speed_mph.clip(5, 85)

    brake_pressure = rng.normal(90, 12, n_events).clip(35, 125)
    engine_temp = rng.normal(175, 25, n_events).clip(90, 260)
    vibration_score = rng.gamma(2.0, 1.2, n_events).clip(0, 15)
    weather_severity = rng.choice([0, 1, 2, 3, 4], size=n_events, p=[0.45, 0.25, 0.16, 0.10, 0.04])
    route_congestion = rng.beta(2, 5, n_events)
    cargo_weight_tons = rng.normal(7000, 1800, n_events).clip(1000, 15000)

    delay_minutes = (
        0.05 * scheduled_minutes
        + 8.0 * route_congestion
        + 3.0 * weather_severity
        + 0.35 * vibration_score
        + 0.05 * np.maximum(engine_temp - 190, 0)
        + 0.03 * np.maximum(80 - avg_speed_mph, 0)
        + rng.normal(0, 6, n_events)
    )
    delay_minutes = np.maximum(delay_minutes, 0)
    delay_risk = (delay_minutes >= 20).astype(int)

    df = pd.DataFrame({
        "event_id": [f"EVT_{i:08d}" for i in range(n_events)],
        "event_time": event_times,
        "train_id": rng.choice(train_ids, size=n_events),
        "route_id": rng.choice(route_ids, size=n_events),
        "latitude": rng.normal(39.0, 5.0, n_events).clip(25, 49),
        "longitude": rng.normal(-98.0, 12.0, n_events).clip(-125, -70),
        "scheduled_minutes": scheduled_minutes,
        "distance_miles": distance_miles,
        "avg_speed_mph": avg_speed_mph,
        "brake_pressure": brake_pressure,
        "engine_temp": engine_temp,
        "vibration_score": vibration_score,
        "weather_severity": weather_severity,
        "route_congestion": route_congestion,
        "cargo_weight_tons": cargo_weight_tons,
        "delay_minutes": delay_minutes,
        "delay_risk": delay_risk,
    })

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    df = generate_synthetic_telemetry()
    print("Synthetic telemetry data generated:", df.shape)
