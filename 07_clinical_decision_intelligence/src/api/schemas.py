from pydantic import BaseModel, Field
class PatientFeatures(BaseModel):
    patient_id: str = Field(min_length=1)
    age: float
    sex: str
    insurance: str
    hospital_id: str
    comorbidity_index: float
    prior_admissions_12m: int
    severity_score: float
    care_management_program: int = Field(ge=0, le=1)
    length_of_stay: float
class PredictionResponse(BaseModel):
    patient_id: str
    predicted_readmission_risk: float
    risk_category: str
    model_version: str = "v3"
class FeedbackRequest(BaseModel):
    patient_id: str
    accepted: bool
    clinician_id: str
    reason: str | None = None
