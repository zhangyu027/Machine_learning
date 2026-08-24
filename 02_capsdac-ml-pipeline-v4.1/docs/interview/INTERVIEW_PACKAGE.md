# CAPSDAC 2.0 Interview Package

## Project title

**CAPSDAC 2.0 ML Data Platform: Governed Preschool Enrollment Forecasting Pipeline**

## 30-second pitch

I built a CAPSDAC-style ML data platform that converts monthly preschool enrollment snapshots into a governed forecasting data product. The project includes schema validation, feature engineering, time-series forecasting, model artifact persistence, forecast publishing, API serving, monitoring starters, and cloud deployment scaffolding. It shows both senior data engineering ownership and practical machine learning engineering delivery.

## 2-minute walkthrough

The business problem is that monthly enrollment records are useful for planning but are not immediately ready for forecasting or executive reporting. The data needs consistent grain, validation rules, reusable features, and a reproducible way to publish outputs.

I structured the solution as a platform rather than a single notebook. The pipeline starts with synthetic CAPSDAC-style enrollment snapshots, validates required columns and business rules, builds site-month features, trains a random forest forecasting baseline using a time-aware split, saves the model artifact, and publishes site, vendor, and statewide forecast outputs.

For engineering readiness, I separated ingestion, feature engineering, forecasting, serving, monitoring, orchestration, and infrastructure. The repo includes tests, a Makefile, CI workflow, GCP/Vertex AI/BigQuery/Cloud Run starter assets, and an API layer for downstream consumption.

The senior-level point is that I am not only training a model. I am showing how to design a governed data product that can move from local development to cloud production with validation, reproducibility, and clear ownership boundaries.

## Senior Data Engineer framing

- Designed a modular raw-to-feature-to-forecast pipeline.
- Added explicit data contract validation at the site-month grain.
- Created reproducible developer commands for testing, pipeline execution, reporting, and API serving.
- Organized the repository around production concerns: ingestion, feature store, orchestration, MLOps, serving, monitoring, and infrastructure.
- Prepared cloud deployment scaffolding for BigQuery, Vertex AI, Cloud Run, Cloud Build, Terraform, and workflow orchestration.

## Machine Learning Engineer framing

- Built a supervised forecasting baseline using lag, rolling, seasonal, and trend features.
- Used a time-aware train/test split to avoid leakage.
- Persisted the trained model artifact for serving and reproducibility.
- Published model metrics and forecast outputs in machine-readable formats.
- Added API endpoints to expose statewide and vendor-level forecasts.

## What I would improve next

- Add model comparison: random forest, gradient boosting, and time-series baselines.
- Add backtesting across multiple cutoff dates.
- Add prediction intervals or conformal uncertainty estimates.
- Add feature importance / SHAP explanation for executive transparency.
- Add BigQuery integration tests and production data quality thresholds.
- Add model drift monitoring and retraining policy.

## Honest scope statement

This public repo uses synthetic de-identified data. It is an interview-ready version that demonstrates architecture, implementation patterns, and platform thinking. A real production version would require official data access, privacy review, governance approval, secure environment variables, and stakeholder sign-off before operational use.
