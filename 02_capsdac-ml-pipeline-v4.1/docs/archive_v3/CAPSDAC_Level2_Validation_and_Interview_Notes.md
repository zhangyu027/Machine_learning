# CAPSDAC Level 2 ML Forecasting Validation Notes

## Validation Results

The Level 2 CAPSDAC ML forecasting package was validated locally with the following results:

- Unit tests: 4 passed
- Pipeline execution: successful
- Input records: 216 synthetic site-month records
- Snapshot range: January 2023 to December 2025
- Sites: 6
- Vendors: 4
- Duplicate site-month records: 0
- Negative enrollment records: 0
- Missing required columns: 0

### Selected Model

The forecasting pipeline selected Ridge Regression using expanding-window time-series validation.

| Metric | Value |
|---|---:|
| MAE | 0.402 |
| RMSE | 0.452 |
| MAPE | 0.443% |
| R² | 0.999 |

### Generated Outputs

- outputs/metrics/model_leaderboard.csv
- outputs/metrics/time_series_cv_results.json
- outputs/reports/drift_report.json
- outputs/forecasts/site_forecast.csv

Note: This public repo uses synthetic data. In production, this workflow would connect to official CAPSDAC data quality thresholds, MLflow or Vertex AI model registry metadata, automated retraining, monitoring alerts, and stakeholder sign-off.

---

# Interview Notes

## How I Validated the Level 2 ML Package

I validated the package at three levels.

First, I ran unit tests for data contracts, feature engineering, and model selection. All tests passed.

Second, I executed the full forecasting pipeline end-to-end using synthetic CAPSDAC-style monthly enrollment data. The pipeline validated the input schema, checked duplicate site-month records, checked negative enrollment values, trained candidate forecasting models, selected the best model, generated forecasts, and saved evaluation outputs.

Third, I generated a reporting summary that includes model metrics, leaderboard results, drift monitoring status, and forecast outputs.

The selected model was Ridge Regression, which outperformed the configured Gradient Boosting candidates on the synthetic dataset. I would not claim this model is production-final. The purpose of this Level 2 package is to demonstrate a reproducible ML-enabled forecasting workflow. In production, I would expand the candidate model set, tune hyperparameters more deeply, track experiments with MLflow or Vertex AI, and validate model performance against real CAPSDAC enrollment history.
