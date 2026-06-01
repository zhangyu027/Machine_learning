# Clinical Decision Intelligence Platform

## Project question
Can we combine healthcare data engineering, predictive modeling, and causal inference to estimate clinical risk and treatment effectiveness in a way that is explainable and decision-ready?

## Why this project matters
This package is designed for pharma, medical device, healthcare analytics, and regulated data roles. It showcases a practical bridge from senior data engineering into AI/ML platform and senior data science work.

## What it includes
- Clinical data contract and validation
- Patient-level feature engineering
- XGBoost-style risk prediction with sklearn fallback
- Propensity score estimation
- Nearest-neighbor propensity matching
- Causal forest-style heterogeneous treatment effect estimation using a T-learner fallback
- Model evaluation
- Executive clinical decision report
- Sample synthetic clinical dataset

## Architecture
```text
Clinical raw data
      ↓
Validation and feature engineering
      ↓
Risk prediction model: XGBoost / gradient boosting fallback
      ↓
Propensity score model
      ↓
Propensity matching
      ↓
Causal forest-style treatment effect estimation
      ↓
Clinical decision intelligence report
```

## Quick start
```bash
cd 07_clinical_decision_intelligence
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_sample_clinical_data.py
python scripts/run_demo.py
pytest
```

## Interview positioning
> I built a clinical decision intelligence pipeline that predicts patient risk using XGBoost-style gradient boosting and estimates treatment effectiveness using propensity score matching and causal forest-style heterogeneous treatment effects. The platform is designed for regulated healthcare and pharma analytics where explainability, traceability, and decision quality matter.
