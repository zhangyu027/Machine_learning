# Level 2 MLE Interview Guide

## Project pitch

I started from a governed CAPSDAC-style monthly enrollment data platform and extended it into an ML-enabled forecasting system. The repo validates monthly snapshots, builds leakage-safe time-series features, compares multiple model families through expanding-window validation, selects the best model, publishes forecast outputs, and generates drift monitoring reports.

## What makes it Level 2

This is not only a notebook model. It has a package layout, tests, generated artifacts, model persistence, monitoring, API serving, and cloud-ready folders. The ML is still applied to an aggregate planning use case, but the pipeline is structured like a production ML data product.

## Strong answers

### Model choice

I do not assume the most complex model is best. I compare a baseline, linear model, random forest, and boosting models. The selected model is based on expanding-window validation metrics, not personal preference.

### Validation

I use expanding-window validation because enrollment is time-dependent. Training data always occurs before validation data. This is closer to the real production setting where future months are unknown.

### Leakage prevention

Lag and rolling features are shifted, which prevents current-month enrollment from leaking into the feature set. Time-based folds also prevent random split leakage across months.

### Drift monitoring

I use population stability index to compare baseline feature distributions against more recent feature distributions. This is not the only drift method, but it is easy to explain, cheap to run, and useful as an early warning signal.

### Production path

The next step would be MLflow experiment tracking, a feature store, scheduled retraining, model registry approvals, drift alerts, and deployment through Cloud Run or Vertex AI.

## Honest limitation

The public repo uses synthetic data. It proves architecture and implementation patterns. Real production performance would need official CAPSDAC data, governance sign-off, stakeholder validation, and monitored deployment.
