import json
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "outputs" / "figures"
TABLE_DIR = ROOT / "outputs" / "tables"

st.set_page_config(page_title="Transportation Telemetry Predictive Timing", layout="wide")

st.title("Transportation Telemetry Predictive Timing Platform")
st.caption("Synthetic train telemetry, lakehouse pipeline, and neural network delay prediction")

st.markdown("""
## Project question

**Can a real-time transportation telemetry platform predict train delay timing and support predictive maintenance decision-making using sensor, location, and operational event data?**
""")

tab_overview, tab_metrics, tab_figures, tab_arch = st.tabs(["Overview", "Metrics", "Figures", "Architecture"])

with tab_overview:
    st.markdown("""
    This project demonstrates:
    - Bronze / Silver / Gold lakehouse pipeline
    - synthetic train telemetry events
    - neural network predictive timing model
    - delay risk classification
    - delay minutes regression
    - portfolio-ready visual outputs
    """)

with tab_metrics:
    metrics_path = TABLE_DIR / "model_metrics.json"
    if metrics_path.exists():
        metrics = json.loads(metrics_path.read_text())
        cols = st.columns(5)
        cols[0].metric("Accuracy", f"{metrics['accuracy']:.2%}")
        cols[1].metric("F1", f"{metrics['f1']:.2%}")
        cols[2].metric("AUC", f"{metrics['auc']:.2%}")
        cols[3].metric("MAE minutes", f"{metrics['mae_delay_minutes']:.2f}")
        cols[4].metric("RMSE minutes", f"{metrics['rmse_delay_minutes']:.2f}")
    else:
        st.warning("Metrics not found. Run: python scripts/run_pipeline.py")

    pred_path = TABLE_DIR / "predictions.csv"
    if pred_path.exists():
        st.dataframe(pd.read_csv(pred_path).head(50), use_container_width=True)

with tab_figures:
    for fig in sorted(FIGURE_DIR.glob("*.png")):
        st.image(str(fig), caption=fig.name, use_container_width=True)

with tab_arch:
    st.markdown((ROOT / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8"))
