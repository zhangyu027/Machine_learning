from __future__ import annotations

import json
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
st.set_page_config(page_title="CAPSDAC V4.1 Program Analytics Platform", layout="wide")
st.title("CAPSDAC V4.1 Program Analytics Platform")
st.caption("Forecasting • rolling backtesting • explainable monitoring • optional certification reconciliation")

metrics_path = ROOT / "outputs/metrics/model_metrics.json"
if not metrics_path.exists():
    st.warning("Run the pipeline before opening the dashboard."); st.stop()
metrics = json.loads(metrics_path.read_text()); avg = metrics["time_series_cv_avg_metrics"]
bt_path = ROOT / "outputs/metrics/backtest_summary.json"
bt = json.loads(bt_path.read_text()) if bt_path.exists() else {}
improvement = bt.get("champion_rmse_improvement_vs_persistence_pct")

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Champion", metrics["selected_model_name"])
c2.metric("RMSE", f"{avg['rmse']:.3f}")
c3.metric("MAE", f"{avg['mae']:.3f}")
c4.metric("MAPE", f"{avg['mape']:.2f}%")
c5.metric("RMSE vs persistence", "N/A" if improvement is None else f"{improvement:+.1f}%")

st.subheader("Rolling Monthly Backtest")
backtest_path = ROOT / "outputs/metrics/rolling_backtest.csv"
if backtest_path.exists():
    backtest = pd.read_csv(backtest_path)
    chart = backtest.pivot(index="test_month", columns="model", values="rmse")
    st.line_chart(chart)
    st.dataframe(backtest, use_container_width=True, hide_index=True)

st.subheader("Forecast Operations")
forecast_path = ROOT / "outputs/forecasts/site_forecast.csv"
if forecast_path.exists():
    fc = pd.read_csv(forecast_path)
    flagged = fc[fc.get("OperationalReviewFlag", False).astype(bool)] if "OperationalReviewFlag" in fc else pd.DataFrame()
    a,b = st.columns(2); a.metric("Site forecasts", len(fc)); b.metric("Operational review flags", len(flagged))
    st.dataframe(fc, use_container_width=True, hide_index=True)

recon_path = ROOT / "outputs/reports/agency_reconciliation_review.csv"
if recon_path.exists():
    st.subheader("Agency Reconciliation Review")
    recon = pd.read_csv(recon_path)
    st.dataframe(recon, use_container_width=True, hide_index=True)
else:
    st.info("Certification reconciliation is ready but optional. Supply --certified-data and --child-counts-data to populate the agency review queue.")

st.subheader("Model Monitoring")
drift_path = ROOT / "outputs/reports/drift_report.json"
if drift_path.exists():
    drift = json.loads(drift_path.read_text())
    d1,d2 = st.columns([1,3]); d1.metric("Operational drift", drift.get("overall_status", "unknown").title())
    drift_df = pd.DataFrame(drift.get("features", []))
    if not drift_df.empty:
        operational = drift_df[drift_df["included_in_operational_status"] == True]
        d2.dataframe(operational[["feature","psi","status","baseline_mean","current_mean"]], use_container_width=True, hide_index=True)

with st.expander("Technical details"):
    st.markdown("#### Model leaderboard")
    st.dataframe(pd.read_csv(ROOT / "outputs/metrics/model_leaderboard.csv"), use_container_width=True, hide_index=True)
    if drift_path.exists(): st.json(json.loads(drift_path.read_text()))
    registry = ROOT / "models/registry/model_registry.json"
    if registry.exists(): st.markdown("#### Champion registry"); st.json(json.loads(registry.read_text()))
    retrain = ROOT / "outputs/retraining/retraining_decision.json"
    if retrain.exists(): st.markdown("#### Retraining decision"); st.json(json.loads(retrain.read_text()))
