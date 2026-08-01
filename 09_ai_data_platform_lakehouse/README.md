# 09 AI Data Platform Lakehouse — Production Grade

> **Important:** This repository uses synthetic data for portfolio and educational purposes. It is not a live healthcare or government production platform.

A reproducible Bronze/Silver/Gold lakehouse reference implementation with enforceable data-quality gates, leakage-safe time-series features, chronological model validation, a Streamlit dashboard, dbt/Airflow design scaffolds, and CI/container support.

## Implemented versus roadmap

| Component | Status |
|---|---|
| Pandas/Parquet Bronze-Silver-Gold pipeline | Executable |
| Data-quality gates | Executable and fail-fast |
| Leakage-safe feature store | Executable |
| Demand forecasting | Executable with chronological holdout |
| Streamlit dashboard | Executable |
| Streaming simulator | Demonstration |
| dbt and Airflow assets | Architecture scaffolds |
| Spark/Delta/cloud object storage | Future production integration |

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-all.txt
python -m scripts.run_pipeline
pytest -q
streamlit run app/streamlit_app.py
```

Dashboard: `http://127.0.0.1:8501`

## Modeling integrity

Lag and rolling features use `shift(1)` before aggregation so the current month is never used to predict itself. Evaluation uses a chronological holdout rather than random train/test splitting. Metrics validate the synthetic demonstration only and are not evidence of real-world operational performance.

## Architecture

```text
Synthetic source -> Bronze immutable landing -> Silver validation/standardization
-> Gold certified aggregates -> Offline feature store -> Forecast training/evaluation
-> Governed tables, metrics, figures, and dashboard
```

## Principal Data Engineer narrative

The project demonstrates an auditable data-product lifecycle: data contracts, layered transformations, quality gates, reproducible features, leakage-aware model validation, containerized delivery, and clear separation between executable local components and enterprise integration paths.
