import streamlit as st
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Medical Imaging Clinical AI", layout="wide")

ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "outputs" / "figures"
TABLE_DIR = ROOT / "outputs" / "tables"
DOC_PATH = ROOT / "docs" / "CLINICAL_INTERPRETATION.md"

st.title("Medical Imaging Clinical AI")
st.caption("Image-only CNN vs multimodal image + metadata clinical AI demo")

st.markdown("""
## Project question

**Can combining medical images with structured clinical metadata improve disease-risk prediction compared with image-only AI?**
""")

tab_overview, tab_results, tab_interpretation, tab_run = st.tabs([
    "Overview",
    "Results",
    "Clinical Interpretation",
    "How to Run"
])

with tab_overview:
    st.markdown("""
    This app is a lightweight viewer for the notebook outputs.

    The main workflow is in:

    ```text
    notebooks/Medical_Imaging_Clinical_AI_End_to_End_Demo.ipynb
    ```

    Run the notebook first to generate tables and figures.
    """)

with tab_results:
    st.subheader("Evaluation table")

    eval_path = TABLE_DIR / "real_evaluation_table.csv"
    if eval_path.exists():
        st.dataframe(pd.read_csv(eval_path), use_container_width=True)
    else:
        st.warning("Evaluation table not found. Run the notebook first.")

    st.subheader("Visual outputs")

    figure_files = [
        "confusion_matrix_multimodal.png",
        "roc_curve_comparison.png",
        "precision_recall_curve_comparison.png",
        "gradcam_heatmap.png",
        "model_comparison_bar_chart.png",
    ]

    for file_name in figure_files:
        path = FIGURE_DIR / file_name
        if path.exists():
            st.image(str(path), caption=file_name, use_container_width=True)
        else:
            st.info(f"Missing: {file_name}. Run the notebook to generate it.")

with tab_interpretation:
    if DOC_PATH.exists():
        st.markdown(DOC_PATH.read_text(encoding="utf-8"))
    else:
        st.warning("Clinical interpretation document not found.")

with tab_run:
    st.markdown("""
    ## Run from terminal

    ```bash
    pip install -r requirements.txt
    jupyter notebook notebooks/Medical_Imaging_Clinical_AI_End_to_End_Demo.ipynb
    ```

    After the notebook generates outputs, launch this app:

    ```bash
    streamlit run app/streamlit_app.py
    ```

    If Streamlit has a Torch watcher warning, run:

    ```bash
    streamlit run app/streamlit_app.py --server.fileWatcherType none
    ```
    """)
