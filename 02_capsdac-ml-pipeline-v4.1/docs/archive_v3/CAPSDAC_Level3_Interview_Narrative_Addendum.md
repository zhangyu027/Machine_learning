
# CAPSDAC Level 3 Interview Narrative Addendum

## Why Time-Series Validation?

### Why didn't you use a random train/test split?

Because enrollment forecasting is inherently temporal.

A random split introduces data leakage because future enrollment patterns can appear in training data.

I used expanding-window validation:

Jan-Jun -> Train
Jul -> Validate

Jan-Jul -> Train
Aug -> Validate

This better simulates production forecasting where only historical data is available when making future predictions.

---

## Why Linear Regression Won

### Why did Linear Regression beat Gradient Boosting?

I intentionally compared simple and complex models.

The synthetic enrollment data exhibits strong linear trends and seasonal patterns.

The simpler linear model generalized better during expanding-window validation and achieved lower RMSE.

I selected the champion model based on validation performance rather than model complexity.

---

## How Did You Avoid Leakage?

All forecasting features were generated from historical observations only.

Examples:

- prior month enrollment
- rolling averages
- lag features

No future enrollment values were available during feature generation.

This prevents target leakage and more accurately represents production conditions.

---

## What Would Production Look Like?

Production Architecture

Data Lake
↓
Feature Pipeline
↓
Model Training
↓
Validation
↓
Model Registry
↓
Deployment
↓
Monitoring
↓
Retraining Trigger

This repository implements a local version of that pattern.

In production I would replace local artifacts with:

- Vertex AI Model Registry
- Cloud Composer / Airflow
- BigQuery
- Cloud Monitoring
- Cloud Scheduler

---

## Business Impact

Potential Business Use Cases

- Enrollment forecasting
- Program demand planning
- Site capacity planning
- Staffing projections
- Funding allocation support

The objective is not merely prediction accuracy.

The objective is enabling proactive planning decisions before enrollment changes occur.

---

## Future Enhancements

- XGBoost and LightGBM benchmarking
- Prophet for seasonality analysis
- MLflow experiment tracking
- Feature Store integration
- Automated retraining workflows
- Model explainability using SHAP
- Forecast uncertainty intervals

---

## Favorite Interview Answer

### What are you most proud of?

The forecasting model itself is not the most important part.

The most valuable part is building a complete machine learning lifecycle:

- data validation
- feature engineering
- model selection
- experiment tracking
- model registry
- monitoring
- retraining decisions

The project demonstrates how a forecasting solution would operate in a production environment rather than as a standalone notebook.

---

## Portfolio Positioning

Current assessment:

- Senior Data Engineer: 9/10
- ML Platform Engineer: 8.5/10
- Machine Learning Engineer: 8/10
- Enterprise Data Architecture: 9/10

The remaining growth area is discussing production tradeoffs, monitoring, governance, and business impact with confidence during interviews.
