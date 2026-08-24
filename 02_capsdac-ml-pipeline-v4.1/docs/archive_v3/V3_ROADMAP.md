# CAPSDAC V3 Roadmap

## V3.1 — Forecasting depth

Delivered: 3-month-ahead site forecast, capacity risk flag, staffing need estimate.

## V3.2 — MLflow / model registry

Delivered: local MLflow-style experiment artifacts, run metadata, runs table, champion/challenger registry.

## V3.3 — Retraining pipeline

Delivered: retraining policy JSON with new-month workflow and drift/performance trigger logic.

## V3.4 — API + monitoring dashboard

Delivered: FastAPI endpoints and Streamlit dashboard for metrics, forecast, drift, registry, and retraining status.

## V3.5 — final interview documentation

Delivered: README, MLE interview guide, architecture note, model card, and generated run summary.

## Future V3.6 production extensions

- XGBoost and LightGBM optional dependencies
- Prophet aggregate forecast benchmark
- True LSTM/Temporal Fusion Transformer only if historical sequence volume justifies it
- SHAP feature explanations
- MLflow/Vertex AI backend
- Airflow/Cloud Composer schedule
- Docker Compose local demo
- Great Expectations or Pandera data validation
