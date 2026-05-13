# CAPSDAC ML System Pipeline Design

## Project Question

**Can monthly CAPSDAC child enrollment snapshots be used to forecast near-term CSPP enrollment and identify the county, site, and vendor drivers of future demand?**

## Pipeline Flow

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

## Pipeline Layers

### 1. Data Layer

```text
data/raw/Child_April_deidentified_sample.csv
data/processed/
```

### 2. Preprocessing Layer

```text
src/preprocessing.py
```

### 3. Forecasting Layer

```text
src/forecasting.py
```

### 4. Visualization Layer

```text
src/visualization.py
outputs/figures/
```

### 5. Reporting Layer

```text
outputs/tables/
outputs/reports/
app/streamlit_app.py
```

## Suggested Future Improvements

1. Add automated monthly data ingestion.
2. Add model backtesting and error metrics.
3. Add confidence intervals.
4. Add Streamlit filters by county, vendor, and site.
5. Add data quality tests.
6. Add automated PDF stakeholder report.
