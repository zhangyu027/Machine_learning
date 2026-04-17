# CAPSDAC ML System — Preschool Enrollment Prediction

## Overview
This project predicts preschool enrollment outcomes using CAPSDAC education data. It demonstrates:
Project Summary

This project implements a distributed machine learning pipeline for hierarchical enrollment forecasting using Azure Synapse, PySpark, and Spark ML. It processes partitioned monthly parquet snapshots, constructs lag-based time-series features, trains a Random Forest regressor, and generates recursive short-horizon forecasts across vendor, site, and program levels. The system was designed to solve real operational planning problems while emphasizing production robustness, schema consistency, and scalable ML workflow design.
- Synapse SQL extraction
- Feature engineering
- Random Forest / XGBoost modeling
- SHAP explainability
- Streamlit dashboard

## Pipeline
1. Extract CAPSDAC data from Synapse
2. Clean and encode features
3. Train classification models
4. Evaluate with accuracy and ROC AUC
5. Serve results in a dashboard

## Run
```bash
python data_pipeline/extract_synapse.py
python data_pipeline/feature_build.py
python modeling/train.py
python modeling/evaluate.py
streamlit run dashboard/app.py
```

## Interview Story
I built a statewide preschool enrollment prediction system on top of CAPSDAC-style education data. I designed the extraction layer from Synapse SQL, created reusable feature engineering, trained ensemble models like Random Forest and XGBoost, and added explainability through SHAP plus a Streamlit dashboard for decision support.

## Best Next Upgrades
- time-based forecasting by county/site
- SHAP interpretation notebook
- Streamlit filters by program/language/IEP
- model comparison table
- synthetic sample dataset for GitHub-safe demo
