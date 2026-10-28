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

## October 2026 synthetic evaluation

Holdout: 300 predictions; Random Forest MAE ~1.805, RMSE ~2.336, R² ~0.851, WAPE ~5.65%; last-observed-month baseline MAE ~1.817. The ~0.66% MAE advantage is marginal and does not demonstrate consistent superiority. The 9/9 quality checks cover implemented rules only. The final feature month has no next-month label and must not be plotted as zero. Synthetic demand contains designed persistence and seasonality and is not evidence of real-world performance. Inspect expanding-window fold results and test across multiple seeds before making broader claims.

## Modeling integrity

The end-of-month t forecast uses observed month t and earlier demand to predict t+1. Lag features are groupwise historical shifts; rolling features use no future observations. Evaluation uses a chronological holdout rather than random train/test splitting. Metrics validate the synthetic demonstration only and are not evidence of real-world operational performance.

## Architecture

```text
Synthetic source -> Bronze immutable landing -> Silver validation/standardization
-> Gold certified aggregates -> Offline feature store -> Forecast training/evaluation
-> Governed tables, metrics, figures, and dashboard
```

## Principal Data Engineer narrative

The project demonstrates an auditable data-product lifecycle: data contracts, layered transformations, quality gates, reproducible features, leakage-aware model validation, containerized delivery, and clear separation between executable local components and enterprise integration paths.
