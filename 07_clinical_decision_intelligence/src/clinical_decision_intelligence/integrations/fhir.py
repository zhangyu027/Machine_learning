from __future__ import annotations

def patient_features_to_fhir_risk_assessment(patient_id: str, risk: float, model_version: str="v3") -> dict:
    """FHIR R4-style simulation; not a certified clinical integration."""
    return {
      "resourceType":"RiskAssessment",
      "status":"final",
      "subject":{"reference":f"Patient/{patient_id}"},
      "method":{"text":f"Clinical Decision Intelligence {model_version}"},
      "prediction":[{"outcome":{"text":"30-day readmission"},"probabilityDecimal":round(float(risk),6)}]
    }

def fhir_bundle(resources: list[dict]) -> dict:
    return {"resourceType":"Bundle","type":"collection","entry":[{"resource":r} for r in resources]}
