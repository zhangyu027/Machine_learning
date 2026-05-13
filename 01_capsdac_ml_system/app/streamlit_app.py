import streamlit as st
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "outputs" / "figures"
TABLE_DIR = ROOT / "outputs" / "tables"

st.set_page_config(page_title="CAPSDAC ML System", layout="wide")

st.title("CAPSDAC ML System")
st.caption("Enrollment forecasting, contribution analysis, and stakeholder-ready visualization")

st.markdown("""
## Project question

**Can monthly CAPSDAC child enrollment snapshots be used to forecast near-term CSPP enrollment and identify the county, site, and vendor drivers of future demand?**
""")

tab_overview, tab_figures, tab_tables, tab_run = st.tabs([
    "Overview",
    "Figures",
    "Tables",
    "How to Run"
])

with tab_overview:
    st.markdown("""
    This dashboard displays outputs from the CAPSDAC enrollment forecasting workflow.

    Main notebooks:

    - `notebooks/01_capsdac_child_monthly_snapshots.ipynb`
    - `notebooks/02_capsdac_3_5_month_recursive_forecast.ipynb`
    - `notebooks/03_capsdac_geo_heatmaps_printable.ipynb`
    """)

with tab_figures:
    st.subheader("Forecasting and contribution figures")
    image_files = sorted(FIGURE_DIR.glob("*.jpg")) + sorted(FIGURE_DIR.glob("*.png"))

    if not image_files:
        st.warning("No figures found in outputs/figures.")
    else:
        for image_path in image_files:
            st.image(str(image_path), caption=image_path.name, use_container_width=True)

with tab_tables:
    st.subheader("Generated tables")
    table_files = sorted(TABLE_DIR.glob("*.csv"))

    if not table_files:
        st.info("No generated tables found yet.")
    else:
        for table_path in table_files:
            st.markdown(f"### {table_path.name}")
            st.dataframe(pd.read_csv(table_path), use_container_width=True)

with tab_run:
    st.markdown("""
    ## Run locally

    ```bash
    pip install -r requirements.txt
    jupyter notebook
    ```

    Run the notebooks in order:

    ```text
    01_capsdac_child_monthly_snapshots.ipynb
    02_capsdac_3_5_month_recursive_forecast.ipynb
    03_capsdac_geo_heatmaps_printable.ipynb
    ```

    Launch this dashboard:

    ```bash
    streamlit run app/streamlit_app.py
    ```

    If Streamlit shows a watcher warning:

    ```bash
    streamlit run app/streamlit_app.py --server.fileWatcherType none
    ```
    """)
