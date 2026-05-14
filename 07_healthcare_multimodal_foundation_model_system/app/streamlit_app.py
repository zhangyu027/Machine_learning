from pathlib import Path
import json
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "outputs" / "tables"
FIGURE_DIR = ROOT / "outputs" / "figures"
DOC_DIR = ROOT / "docs"

st.set_page_config(page_title="Healthcare Multimodal AI", layout="wide")

st.title("Healthcare Multimodal Foundation Model System")
st.caption("Image + clinical note + labs + structured EHR risk prediction")

st.markdown("""
## Project Question

**Can multimodal healthcare AI combine medical images, clinical notes, labs, and structured EHR data to improve risk prediction and clinical interpretability?**
""")

tab_overview, tab_metrics, tab_fairness, tab_interpretation = st.tabs([
    "Overview", "Metrics", "Fairness & Uncertainty", "Clinical Interpretation"
])

with tab_overview:
    st.markdown((DOC_DIR / "ARCHITECTURE.md").read_text(encoding="utf-8"))

with tab_metrics:
    metrics_path = TABLE_DIR / "model_metrics.json"
    if metrics_path.exists():
        metrics = json.loads(metrics_path.read_text())
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Accuracy", f"{metrics['accuracy']:.2%}")
        c2.metric("F1", f"{metrics['f1']:.2%}")
        c3.metric("AUC", f"{metrics['auc']:.2%}")
        c4.metric("Brier Score", f"{metrics['brier_score']:.3f}")
    else:
        st.warning("Run python scripts/run_pipeline.py first.")

    for fig in ["confusion_matrix.png", "roc_curve.png", "precision_recall_curve.png", "model_metrics_bar_chart.png", "training_loss_curve.png"]:
        path = FIGURE_DIR / fig
        if path.exists():
            st.image(str(path), caption=fig, use_container_width=True)

with tab_fairness:
    fair_path = TABLE_DIR / "fairness_subgroup_metrics.csv"
    uncertainty_path = TABLE_DIR / "uncertainty_review_queue.csv"

    if fair_path.exists():
        st.subheader("Fairness subgroup metrics")
        st.dataframe(pd.read_csv(fair_path), use_container_width=True)

    if uncertainty_path.exists():
        st.subheader("High uncertainty review queue")
        st.dataframe(pd.read_csv(uncertainty_path).head(25), use_container_width=True)

    fig = FIGURE_DIR / "fairness_accuracy_by_sex.png"
    if fig.exists():
        st.image(str(fig), caption="Fairness by sex", use_container_width=True)

with tab_interpretation:
    st.markdown((DOC_DIR / "CLINICAL_INTERPRETATION.md").read_text(encoding="utf-8"))
