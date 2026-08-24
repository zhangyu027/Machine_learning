from __future__ import annotations

from pathlib import Path
import argparse
import json
import sys

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ingestion.capsdac_child_adapter import write_site_month_aggregate
from src.capsdac_ml.contribution_analysis import statewide_forecast, vendor_contribution
from src.capsdac_ml.data_contracts import validate_enrollment_snapshot
from src.capsdac_ml.experiment_tracking import write_experiment_artifacts
from src.capsdac_ml.feature_engineering import FORECAST_HORIZON_MONTHS, TARGET_COL, build_monthly_features
from src.capsdac_ml.forecasting import generate_site_forecast
from src.capsdac_ml.model_registry import promote_champion_model
from src.capsdac_ml.model_selection import run_model_selection
from src.capsdac_ml.monitoring import drift_report
from src.capsdac_ml.retraining import retraining_decision
from src.capsdac_ml.backtesting import rolling_backtest, backtest_summary
from src.capsdac_ml.decision_science import build_reconciliation_review


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run CAPSDAC V4 12-month forecasting pipeline")
    group = p.add_mutually_exclusive_group(required=False)
    group.add_argument("--child-data", type=Path, help="Private CAPSDAC child CSV/ZIP; never committed")
    group.add_argument("--aggregate-data", type=Path, help="Already aggregated site-month CSV")
    p.add_argument("--keep-private-aggregate", action="store_true", help="Keep generated site-month aggregate in data/processed")
    p.add_argument("--certified-data", type=Path, help="Optional agency certification CSV for reconciliation review")
    p.add_argument("--child-counts-data", type=Path, help="Optional agency child-count CSV for reconciliation review")
    return p.parse_args()


def load_input(args: argparse.Namespace) -> pd.DataFrame:
    if args.child_data:
        aggregate_path = ROOT / "data/processed/private_site_month_aggregate.csv"
        raw = write_site_month_aggregate(args.child_data, aggregate_path)
        if not args.keep_private_aggregate:
            aggregate_path.unlink(missing_ok=True)
        return raw
    if args.aggregate_data:
        return pd.read_csv(args.aggregate_data, dtype={"VendorNumber": str, "PreschoolCDSCode": str})

    demo = ROOT / "data/demo/capsdac_12month_site_demo.csv"
    if not demo.exists():
        raise FileNotFoundError("Demo data not found. Run: python scripts/generate_demo_data.py")
    return pd.read_csv(demo, dtype={"VendorNumber": str, "PreschoolCDSCode": str})


def main() -> None:
    args = parse_args()
    for folder in [
        ROOT / "outputs/metrics", ROOT / "outputs/reports", ROOT / "outputs/forecasts",
        ROOT / "outputs/experiments", ROOT / "outputs/retraining", ROOT / "models", ROOT / "models/registry",
    ]:
        folder.mkdir(parents=True, exist_ok=True)

    raw = load_input(args)
    validation_report = validate_enrollment_snapshot(raw)
    write_json(ROOT / "outputs/reports/data_validation_report.json", validation_report)

    features = build_monthly_features(raw, horizon_months=FORECAST_HORIZON_MONTHS)
    # Feature rows are aggregate-level only; still excluded from the release package by default.
    features.to_csv(ROOT / "data/processed/monthly_enrollment_features.csv", index=False)

    best_model, selection_report, leaderboard = run_model_selection(features)
    model_path = ROOT / "models/capsdac_v4_challenger_forecast_model.joblib"
    joblib.dump(best_model, model_path)

    leaderboard.to_csv(ROOT / "outputs/metrics/model_leaderboard.csv", index=False)
    selected = selection_report["selected_model"]
    model_metrics = {
        "package_level": "Senior Data Scientist / MLE portfolio",
        "selected_model_name": selected["model_name"],
        "selected_params": selected["params"],
        "time_series_cv_avg_metrics": selected["avg_metrics"],
        "cv_strategy": "expanding-window monthly validation",
        "forecast_horizon_months": FORECAST_HORIZON_MONTHS,
        "history_months": validation_report["month_count"],
        "train_target": TARGET_COL,
        "model_artifact": str(model_path.relative_to(ROOT)),
        "business_tasks": ["next_month_site_enrollment", "program_demand", "operational_review_flag"],
    }
    write_json(ROOT / "outputs/metrics/model_metrics.json", model_metrics)
    write_json(ROOT / "outputs/metrics/time_series_cv_results.json", selection_report)

    backtest = rolling_backtest(features, best_model)
    backtest.to_csv(ROOT / "outputs/metrics/rolling_backtest.csv", index=False)
    bt_summary = backtest_summary(backtest)
    write_json(ROOT / "outputs/metrics/backtest_summary.json", bt_summary)
    model_metrics["baseline_comparison"] = bt_summary
    write_json(ROOT / "outputs/metrics/model_metrics.json", model_metrics)

    drift = drift_report(features)
    write_json(ROOT / "outputs/reports/drift_report.json", drift)

    run_metadata = write_experiment_artifacts(ROOT, leaderboard, selection_report)
    registry = promote_champion_model(ROOT, best_model, run_metadata, selected["avg_metrics"])
    decision = retraining_decision(ROOT, model_metrics, drift)

    site = generate_site_forecast(best_model, features, horizon_months=FORECAST_HORIZON_MONTHS)
    site.to_csv(ROOT / "outputs/forecasts/site_forecast.csv", index=False)

    reconciliation = build_reconciliation_review(args.certified_data, args.child_counts_data)
    if not reconciliation.empty:
        reconciliation.to_csv(ROOT / "outputs/reports/agency_reconciliation_review.csv", index=False)
    vendor_contribution(site).to_csv(ROOT / "outputs/forecasts/vendor_forecast.csv", index=False)
    statewide_forecast(site).to_csv(ROOT / "outputs/forecasts/statewide_forecast.csv", index=False)

    run_summary = {
        "validation": validation_report,
        "forecast_horizon_months": FORECAST_HORIZON_MONTHS,
        "selected_model": selected["model_name"],
        "selected_params": selected["params"],
        "metrics": selected["avg_metrics"],
        "registry_decision": registry["decision"],
        "retraining_triggered": decision["triggered"],
        "outputs": [
            "outputs/metrics/model_leaderboard.csv",
            "outputs/metrics/time_series_cv_results.json",
            "outputs/metrics/rolling_backtest.csv",
            "outputs/metrics/backtest_summary.json",
            "outputs/reports/drift_report.json",
            "outputs/experiments/runs.csv",
            "models/registry/model_registry.json",
            "outputs/retraining/retraining_decision.json",
            "outputs/forecasts/site_forecast.csv",
        ],
    }
    print(json.dumps(run_summary, indent=2))


if __name__ == "__main__":
    main()
