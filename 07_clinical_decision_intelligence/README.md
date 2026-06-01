# 07 Clinical Decision Intelligence V2

A healthcare/pharma/medical-device decision intelligence project combining predictive ML and causal inference.

## What is included

- Real XGBoost readmission risk model
- SHAP explainability report
- Propensity score modeling and nearest-neighbor matching
- Doubly robust treatment effect estimation
- Causal-forest-style heterogeneous treatment effect estimation
- Patient-level risk + treatment benefit recommendations
- Saved model artifacts, model outputs, reports, and figures

## Key outputs

- `data/raw/patient_encounters.csv`
- `data/processed/clinical_modeling_dataset.csv`
- `models/xgboost_readmission_model.joblib`
- `models/propensity_model.joblib`
- `models/causal_forest_style_t_learner.joblib`
- `reports/model_outputs/model_summary.json`
- `reports/model_outputs/shap_feature_importance.csv`
- `reports/model_outputs/patient_risk_effect_recommendations.csv`
- `reports/figures/*.png`

## Interview story

I built a clinical decision intelligence platform that predicts readmission risk and estimates which patients benefit from a care-management intervention. The project combines XGBoost, SHAP, propensity score matching, doubly robust estimation, and heterogeneous treatment effect modeling.

## Run

```bash
pip install -r requirements.txt
python scripts/run_full_pipeline.py
```
