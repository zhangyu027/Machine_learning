from pathlib import Path
import pandas as pd


def bronze_ingest(
    raw_path="data/raw/public_health_events.csv",
    bronze_path="data/bronze/events_bronze.parquet",
):
    df = pd.read_csv(raw_path)

    out = Path(bronze_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(out, index=False)
    return df


def silver_clean(
    bronze_path="data/bronze/events_bronze.parquet",
    silver_path="data/silver/events_silver.parquet",
):
    df = pd.read_parquet(bronze_path)

    df["event_month"] = pd.to_datetime(df["event_month"], errors="coerce")

    df = df.dropna(
        subset=["event_id", "event_month", "county", "program", "site_id"]
    )

    df = df.drop_duplicates(subset=["event_id"])

    numeric_cols = [
        "risk_score",
        "service_count",
        "prior_utilization",
        "social_need_index",
        "target_next_month_demand",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=numeric_cols)

    df["year"] = df["event_month"].dt.year
    df["month"] = df["event_month"].dt.month

    out = Path(silver_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(out, index=False)
    return df


def gold_certified_tables(
    silver_path="data/silver/events_silver.parquet",
    gold_path="data/gold/gold_monthly_program_demand.parquet",
):
    df = pd.read_parquet(silver_path)

    gold = (
        df.groupby(["event_month", "county", "program"], as_index=False)
        .agg(
            total_services=("service_count", "sum"),
            avg_risk_score=("risk_score", "mean"),
            avg_social_need=("social_need_index", "mean"),
            total_prior_utilization=("prior_utilization", "sum"),
            target_next_month_demand=("target_next_month_demand", "sum"),
            record_count=("event_id", "count"),
        )
        .sort_values(["event_month", "county", "program"])
    )

    # ==========================================
    # Save Gold Parquet
    # ==========================================

    out = Path(gold_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    gold.to_parquet(out, index=False)

    # ==========================================
    # Save Gold CSV SAFELY
    # ==========================================

    project_root = out.parents[2]

    csv_out = (
        project_root
        / "outputs"
        / "tables"
        / "gold_monthly_program_demand.csv"
    )

    csv_out.parent.mkdir(parents=True, exist_ok=True)

    gold.to_csv(csv_out, index=False)

    print(f"Saved Gold parquet to: {out}")
    print(f"Saved Gold CSV to: {csv_out}")

    return gold


def run_lakehouse_pipeline():
    bronze_ingest()
    silver_clean()
    return gold_certified_tables()


if __name__ == "__main__":
    gold_df = run_lakehouse_pipeline()
    print(gold_df.head())
    print(gold_df.shape)