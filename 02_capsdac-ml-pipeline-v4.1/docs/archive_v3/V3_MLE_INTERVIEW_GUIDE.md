# CAPSDAC Level 3 MLE Interview Guide

## 60-second project pitch

I built a Level 3 Machine Learning Engineer version of a CAPSDAC-style preschool enrollment forecasting platform. The goal is to predict 3-month-ahead site-level enrollment and convert those predictions into planning signals such as program demand, capacity risk, and staffing need.

The system validates monthly snapshots, builds leakage-safe lag and rolling features, adds operational context such as site capacity and teacher-student ratio, compares multiple candidate models through expanding-window time-series validation, tracks local MLflow-style experiment artifacts, promotes a champion model through a registry workflow, monitors drift, generates retraining decisions, and exposes results through API and dashboard layers.

## Why this is more than a notebook

This is not just a model script. It includes data contracts, feature engineering, model selection, monitoring, registry logic, retraining policy, API serving, dashboard reporting, and stakeholder documentation. That is the difference between a data science demo and a production ML platform pattern.

## How I selected the model

I selected the champion model by expanding-window time-series validation using RMSE as the primary metric and MAE/MAPE/R² as supporting metrics. I compared baselines, linear models, random forest, boosting models, and a lightweight neural-network proxy. The selected model is the model with the strongest validation performance, not the most complex model.

## Why expanding-window validation

Enrollment forecasting is time-dependent. A random split would leak future seasonal and trend information into training. Expanding-window validation simulates production: train on historical months, validate on the next month, then expand the training window and repeat.

## How I handled XGBoost, LightGBM, Prophet, and LSTM

The public repo keeps the default runtime lightweight using scikit-learn. In production I would add optional XGBoost and LightGBM candidates because they often perform well on tabular structured data. Prophet could be tested for strong seasonality at aggregate levels. LSTM would only be justified if we had enough historical sequence data across many sites and needed nonlinear temporal sequence learning. I would not choose LSTM just because it sounds advanced.

## What the business impact is

The model supports planning decisions, not eligibility decisions. It helps identify expected enrollment demand, capacity pressure, staffing need, and unusual enrollment changes. The outputs are useful for program operations, forecasting discussions, and early warning review.

## What I would do in production

In production, I would connect this pipeline to official CAPSDAC data sources, MLflow or Vertex AI Model Registry, Airflow or Cloud Composer scheduling, access-controlled storage, formal monitoring alerts, and stakeholder sign-off. I would also define promotion thresholds, drift thresholds, rollback procedures, and retraining approval workflow.
