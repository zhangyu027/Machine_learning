from pathlib import Path
import json
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "outputs" / "tables"
FIGURE_DIR = ROOT / "outputs" / "figures"
DOC_DIR = ROOT / "docs"

st.set_page_config(page_title="AI Data Platform Lakehouse", layout="wide")

st.title("AI Data Platform / Lakehouse")
st.caption("Bronze/Silver/Gold + Feature Store + MLflow-ready forecasting + Governance")

st.markdown("""
## Project Question

**Can a modern healthcare/public-sector lakehouse improve scalable AI analytics and forecasting workflows?**
""")

tab_overview, tab_quality, tab_model, tab_arch = st.tabs(["Overview", "Data Quality", "Forecasting", "Architecture"])

with tab_overview:
    st.markdown("""
    This dashboard summarizes a local lakehouse-style data platform.

    Layers:
    - Bronze raw events
    - Silver cleaned records
    - Gold certified analytics table
    - Feature store
    - ML forecasting output
    """)

    gold = TABLE_DIR / "gold_monthly_program_demand.csv"
    if gold.exists():
        st.subheader("Gold Certified Dataset")
        st.dataframe(pd.read_csv(gold).head(100), use_container_width=True)

with tab_quality:
    q = TABLE_DIR / "data_quality_report.csv"
    if q.exists():
        st.dataframe(pd.read_csv(q), use_container_width=True)
    else:
        st.warning("Run python scripts/run_pipeline.py first.")

    fig = FIGURE_DIR / "data_quality_pass_rate.png"
    if fig.exists():
        st.image(str(fig), caption="Data quality pass rate", use_container_width=True)

with tab_model:
    metrics_path = TABLE_DIR / "forecast_model_metrics.json"
    if metrics_path.exists():
        metrics = json.loads(metrics_path.read_text())
        c1, c2, c3 = st.columns(3)
        c1.metric("MAE", f"{metrics['mae']:.2f}")
        c2.metric("RMSE", f"{metrics['rmse']:.2f}")
        c3.metric("R²", f"{metrics['r2']:.3f}")

    for fig in ["monthly_program_demand_trend.png", "actual_vs_predicted_demand.png", "forecast_model_metrics.png"]:
        path = FIGURE_DIR / fig
        if path.exists():
            st.image(str(path), caption=fig, use_container_width=True)

with tab_arch:
    st.markdown((DOC_DIR / "ARCHITECTURE.md").read_text(encoding="utf-8"))
    st.markdown((DOC_DIR / "GOVERNANCE.md").read_text(encoding="utf-8"))
