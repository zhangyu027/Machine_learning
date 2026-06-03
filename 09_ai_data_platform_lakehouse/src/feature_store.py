from pathlib import Path
import pandas as pd


def build_feature_store(
    gold_path="data/gold/gold_monthly_program_demand.parquet",
    feature_path="data/feature_store/monthly_program_features.parquet",
):
    df = pd.read_parquet(gold_path)

    df["event_month"] = pd.to_datetime(df["event_month"])

    df = df.sort_values(
        ["county", "program", "event_month"]
    )

    # ==========================================
    # Feature Engineering
    # ==========================================

    for col in [
        "total_services",
        "avg_risk_score",
        "avg_social_need",
        "total_prior_utilization",
    ]:
        df[f"{col}_lag1"] = (
            df.groupby(["county", "program"])[col]
            .shift(1)
        )

        df[f"{col}_rolling3"] = (
            df.groupby(["county", "program"])[col]
            .rolling(3, min_periods=1)
            .mean()
            .reset_index(level=[0, 1], drop=True)
        )

    df = df.dropna().reset_index(drop=True)

    # ==========================================
    # Save Feature Store Parquet
    # ==========================================

    out = Path(feature_path)

    out.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(out, index=False)

    # ==========================================
    # Save CSV SAFELY
    # ==========================================

    project_root = out.parents[2]

    csv_out = (
        project_root
        / "outputs"
        / "tables"
        / "monthly_program_features.csv"
    )

    csv_out.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(csv_out, index=False)

    print(f"Saved feature store parquet to: {out}")
    print(f"Saved feature store CSV to: {csv_out}")

    return df


if __name__ == "__main__":
    feature_df = build_feature_store()
    print(feature_df.head())
    print(feature_df.shape)