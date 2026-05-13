# CAPSDAC ML System


---

## Data Privacy and De-identification

CAPSDAC data may include PII or sensitive child-level information.  
This public package is de-identified and does **not** include raw child-level CAPSDAC data.

The CDE data warehouse should only be accessed from the issued laptop / approved secure environment.

Public package sample data:

```text
data/raw/Child_April_deidentified_sample.csv
```

Privacy documentation:

```text
docs/DATA_PRIVACY_AND_DEIDENTIFICATION.md
```

De-identification helper:

```text
src/deidentify.py
```

Do not commit raw child-level files, direct identifiers, warehouse credentials, or secure connection details to GitHub.


## Project Question

**Can monthly CAPSDAC child enrollment snapshots be used to forecast near-term CSPP enrollment and identify the county, site, and vendor drivers of future demand?**

This project is a CAPSDAC enrollment forecasting and contribution analysis workflow. It is designed for education analytics, program monitoring, and stakeholder-facing reporting.

---

## What This Project Does

The system:

1. Builds monthly child enrollment snapshots.
2. Forecasts near-term CSPP enrollment for 3-5 months.
3. Identifies top county, site, and vendor contributors.
4. Creates geographic contribution heat maps.
5. Produces stakeholder-ready charts and tables.
6. Organizes outputs into a reproducible portfolio package.

---

## Repository Structure

```text
01_capsdac_ml_system/
├── app/
│   └── streamlit_app.py
├── data/
│   ├── raw/
│   │   └── Child_April_deidentified_sample.csv
│   └── processed/
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   └── MODEL_CARD.md
├── notebooks/
│   ├── 01_capsdac_child_monthly_snapshots.ipynb
│   ├── 02_capsdac_3_5_month_recursive_forecast.ipynb
│   └── 03_capsdac_geo_heatmaps_printable.ipynb
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── reports/
├── src/
│   ├── preprocessing.py
│   ├── forecasting.py
│   └── visualization.py
├── artifacts/
│   ├── figures/
│   └── tables/
├── requirements.txt
└── README.md
```

---


---

## Step-by-Step Run Instructions

A detailed run guide is included here:

```text
docs/STEP_BY_STEP_RUN_GUIDE.md
```
```
cd /Users/yuzhang/Library/CloudStorage/Dropbox/MachineLearning/01_capsdac_ml_system

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name capsdac_env --display-name "Python (CAPSDAC)"
```
source .venv/bin/activate
pip install pysparkQuick start:

```bash
pip install -r requirements.txt
jupyter notebook
```

Run notebooks in order:

```text
notebooks/01_capsdac_child_monthly_snapshots.ipynb
notebooks/02_capsdac_3_5_month_recursive_forecast.ipynb
notebooks/03_capsdac_geo_heatmaps_printable.ipynb
```

Then run helper scripts:

```bash
python scripts/run_capsdac_pipeline.py
python scripts/generate_visualization_report.py
```

Or run both helper scripts together:

```bash
bash run_pipeline.sh
```

Launch dashboard:

```bash
streamlit run app/streamlit_app.py
```

---

## Pipeline Documentation

The pipeline design is documented here:

```text
docs/PIPELINE_DESIGN.md
```

Pipeline flow:

```text
Raw child snapshot CSV
        ↓
Data validation and schema review
        ↓
Monthly snapshot construction
        ↓
Feature engineering
        ↓
3-5 month recursive forecasting
        ↓
Site / vendor / county aggregation
        ↓
Contribution analysis
        ↓
Geographic and heatmap visualization
        ↓
Dashboard and stakeholder reporting
```

---

## Visualization Documentation

A detailed guide to the visual outputs is available here:

```text
docs/VISUALIZATION_GUIDE.md
```

Generate the visualization inventory:

```bash
python scripts/generate_visualization_report.py
```

Outputs:

```text
outputs/reports/visualization_inventory.csv
outputs/reports/visualization_inventory.md
```


## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Open notebooks

```bash
jupyter notebook
```

Run notebooks in this order:

```text
notebooks/01_capsdac_child_monthly_snapshots.ipynb
notebooks/02_capsdac_3_5_month_recursive_forecast.ipynb
notebooks/03_capsdac_geo_heatmaps_printable.ipynb
```

### 3. Launch dashboard

```bash
streamlit run app/streamlit_app.py
```

If Streamlit shows a watcher warning:

```bash
streamlit run app/streamlit_app.py --server.fileWatcherType none
```

---

## Key Visual Outputs

### Historical and Predicted Enrollment Trend

![CSPP Enrollment Growth](outputs/figures/cspp_enrollment_growth.jpg)

### County-Level Enrollment Contribution Heat Map

![County Enrollment Heatmap](outputs/figures/geomap_county_enrollment.jpg)

### Top 20 Site Monthly Contribution Heatmap

![Top 20 Site Heatmap](outputs/figures/top_20_sites_heatmap.jpg)

### Top Site Contribution Percentage

![Top Sites Contribution](outputs/figures/top_sites_contribution.jpg)

### Top Vendor Contribution Percentage

![Top Vendor Contribution](outputs/figures/top_vendor_contribution.jpg)

### Top Sites by Forecast Enrollment

![Top 10 Sites Forecast](outputs/figures/top_10_sites_forecast_enrollment.jpg)

### Top Site Enrollment Growth

![Top 10 Site Growth](outputs/figures/top_10_sites_growth_forecast.jpg)

### Top Vendors by Forecast Enrollment

![Top 10 Vendor Forecast](outputs/figures/top_10_vendor_forecast_enrollment.jpg)

### Top Vendor Enrollment Growth

![Top 10 Vendor Growth](outputs/figures/top_10_vendor_growth_forecast.jpg)

---

## Tables

Generated tables are stored in:

```text
outputs/tables/
artifacts/tables/
```

Included starter tables:

- `deidentified_sample_schema.csv`
- `deidentified_sample_rows.csv`

---

## Documentation

Additional documentation:

- `docs/PROJECT_OVERVIEW.md`
- `docs/MODEL_CARD.md`
- `outputs/reports/OUTPUT_FIGURES_README.md`

---

## Notes from Uploaded Data

Rows in Child_April_deidentified_sample.csv: 2,314
Columns: 188

---

## Limitations

- Forecasts depend on snapshot data quality.
- Site/vendor naming changes may affect trend continuity.
- Short forecast horizons are better suited than long-range planning.
- Results should be reviewed with program and policy context.

---

## Resume Bullet

Built a CAPSDAC enrollment forecasting system using monthly child snapshot data to forecast near-term CSPP enrollment, identify county/site/vendor contribution drivers, and generate stakeholder-ready geospatial heat maps, trend charts, and contribution analyses.
