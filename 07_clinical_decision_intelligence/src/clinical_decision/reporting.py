from __future__ import annotations


def build_clinical_report(risk_result: dict, att: float, cate_summary: dict) -> str:
    direction = "reduced" if att < 0 else "increased"
    return f"""
# Clinical Decision Intelligence Report

## Predictive model
- Readmission ROC-AUC: {risk_result['roc_auc']:.3f}
- Average precision: {risk_result['avg_precision']:.3f}

## Propensity-matched treatment effect
- Average treatment effect on treated: {att:.4f}
- Interpretation: treatment is associated with {direction} readmission risk among matched treated patients.

## Heterogeneous treatment effect insight
- CATE by site/segment: {cate_summary}

## Recommended executive message
Use the predictive model for patient-level risk stratification, but use the causal estimates to guide treatment-policy decisions. Prediction answers who is high risk; causal inference estimates whether the intervention changes outcomes.
""".strip()
