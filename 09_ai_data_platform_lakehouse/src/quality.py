from pathlib import Path
import pandas as pd


def run_quality_checks(
    silver_path="data/silver/events_silver.parquet",
    output_path="outputs/tables/data_quality_report.csv",
):
    df = pd.read_parquet(silver_path)
    checks = []

    checks.append({
        "check_name": "row_count_positive",
        "passed": len(df) > 0,
        "value": len(df),
    })

    checks.append({
        "check_name": "event_id_unique",
        "passed": df["event_id"].is_unique,
        "value": df["event_id"].nunique(),
    })

    for col in ["county", "program", "site_id", "event_month"]:
        checks.append({
            "check_name": f"{col}_not_null",
            "passed": df[col].notna().all(),
            "value": int(df[col].isna().sum()),
        })

    for col in ["risk_score", "social_need_index"]:
        checks.append({
            "check_name": f"{col}_between_0_and_1",
            "passed": df[col].between(0, 1).all(),
            "value": f"{df[col].min():.3f} - {df[col].max():.3f}",
        })

    out = pd.DataFrame(checks)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)
    return out


if __name__ == "__main__":
    print(run_quality_checks())
