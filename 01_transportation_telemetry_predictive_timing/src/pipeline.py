from pathlib import Path
import pandas as pd

FEATURE_COLS = [
    "scheduled_minutes", "distance_miles", "avg_speed_mph", "brake_pressure",
    "engine_temp", "vibration_score", "weather_severity", "route_congestion",
    "cargo_weight_tons", "hour", "day_of_week"
]


def bronze_ingest(raw_path="data/raw/train_telemetry_events.csv", bronze_path="data/bronze/telemetry_bronze.parquet"):
    df = pd.read_csv(raw_path)
    out = Path(bronze_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    return df


def silver_clean(bronze_path="data/bronze/telemetry_bronze.parquet", silver_path="data/silver/telemetry_silver.parquet"):
    df = pd.read_parquet(bronze_path)
    df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce")
    df = df.dropna(subset=["event_id", "event_time", "train_id", "route_id"])
    df = df.drop_duplicates(subset=["event_id"])

    numeric_cols = [
        "latitude", "longitude", "scheduled_minutes", "distance_miles",
        "avg_speed_mph", "brake_pressure", "engine_temp", "vibration_score",
        "weather_severity", "route_congestion", "cargo_weight_tons",
        "delay_minutes", "delay_risk"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=numeric_cols)
    df = df[df["scheduled_minutes"] > 0]
    df = df[df["distance_miles"] > 0]

    out = Path(silver_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    return df


def gold_features(silver_path="data/silver/telemetry_silver.parquet", gold_path="data/gold/train_delay_features.parquet"):
    df = pd.read_parquet(silver_path)
    df["event_time"] = pd.to_datetime(df["event_time"])
    df["hour"] = df["event_time"].dt.hour
    df["day_of_week"] = df["event_time"].dt.dayofweek

    route_stats = (
        df.groupby("route_id")
        .agg(
            route_avg_delay=("delay_minutes", "mean"),
            route_avg_congestion=("route_congestion", "mean"),
            route_event_count=("event_id", "count"),
        )
        .reset_index()
    )
    df = df.merge(route_stats, on="route_id", how="left")

    out = Path(gold_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    return df


def run_pipeline():
    bronze_ingest()
    silver_clean()
    return gold_features()


if __name__ == "__main__":
    df = run_pipeline()
    print("Gold feature table created:", df.shape)
