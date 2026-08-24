from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    metrics = json.loads((ROOT / "outputs/metrics/model_metrics.json").read_text())
    validation = json.loads((ROOT / "outputs/reports/data_validation_report.json").read_text())
    leaderboard = pd.read_csv(ROOT / "outputs/metrics/model_leaderboard.csv")
    site = pd.read_csv(ROOT / "outputs/forecasts/site_forecast.csv")
    avg = metrics["time_series_cv_avg_metrics"]

    report = f"""# CAPSDAC V4 Forecast Run Summary

## Data coverage

- Months: {validation['snapshot_month_min']} through {validation['snapshot_month_max']} ({validation['month_count']} months)
- Sites: {validation['site_count']}
- Agencies/vendors: {validation['vendor_count']}
- Modeling grain: site-month aggregate

## Forecast design

- Forecast target: next-month preschool site enrollment (H+1)
- Validation: expanding-window monthly holdouts
- Selected model: {metrics['selected_model_name']}
- RMSE: {avg['rmse']:.3f}
- MAE: {avg['mae']:.3f}
- MAPE: {avg['mape']:.3f}%
- R²: {avg['r2']:.3f}

## Operational output

- Forecast rows: {len(site)}
- Review flags (absolute forecast change >=20%): {int(site['OperationalReviewFlag'].sum())}

## Model leaderboard

{leaderboard.head(10).to_markdown(index=False)}
"""
    out = ROOT / "outputs/reports/run_summary.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report)
    print(out)


if __name__ == "__main__":
    main()
