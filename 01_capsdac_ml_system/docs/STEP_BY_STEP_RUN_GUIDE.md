# Step-by-Step Run Guide

## 1. Open the project

```bash
cd 01_capsdac_ml_system
```

## 2. Create a Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

For Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Confirm the raw data file exists

```text
data/raw/Child_April_deidentified_sample.csv
```

## 5. Run notebooks in order

```bash
jupyter notebook
```

Run:

```text
1. notebooks/01_capsdac_child_monthly_snapshots.ipynb
2. notebooks/02_capsdac_3_5_month_recursive_forecast.ipynb
3. notebooks/03_capsdac_geo_heatmaps_printable.ipynb
```

## 6. Run pipeline helper

```bash
python scripts/run_capsdac_pipeline.py
```

## 7. Generate visualization inventory

```bash
python scripts/generate_visualization_report.py
```

## 8. Launch dashboard

```bash
streamlit run app/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

If Streamlit has a file watcher warning:

```bash
streamlit run app/streamlit_app.py --server.fileWatcherType none
```

## 9. Review outputs

```text
outputs/figures/
outputs/tables/
outputs/reports/
```

## 10. Push to GitHub

```bash
git status
git add .
git commit -m "Update CAPSDAC ML system pipeline and visual outputs"
git push origin main
```
