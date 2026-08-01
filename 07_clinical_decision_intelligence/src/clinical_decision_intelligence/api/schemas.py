from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class PatientFeatures(BaseModel):
    patient_id: str = Field(min_length=1, max_length=128)
    age: float = Field(ge=0, le=125)
    sex: str = Field(min_length=1, max_length=32)
    insurance: str = Field(min_length=1, max_length=100)
    hospital_id: str = Field(min_length=1, max_length=128)
    comorbidity_index: float = Field(ge=0)
    prior_admissions_12m: int = Field(ge=0)
    severity_score: float = Field(ge=0)
    care_management_program: int = Field(ge=0, le=1)
    length_of_stay: float = Field(ge=0)


class PredictionResponse(BaseModel):
    patient_id: str
    predicted_readmission_risk: float = Field(ge=0, le=1)
    risk_category: Literal["low", "moderate", "high"]
    model_version: str
    requires_clinician_review: bool = True


class FeedbackRequest(BaseModel):
    patient_id: str = Field(min_length=1, max_length=128)
    accepted: bool
    clinician_id: str = Field(min_length=1, max_length=128)
    reason: str | None = Field(default=None, max_length=2_000)


class FeedbackResponse(BaseModel):
    patient_id: str
    accepted: bool
    clinician_id: str
    reason: str | None = None
    recorded_at: str


class HealthResponse(BaseModel):
    status: Literal["healthy"]
    version: str


class ReadinessResponse(BaseModel):
    status: Literal["ready", "not_ready"]
    model_loaded: bool


class VersionResponse(BaseModel):
    service: str
    version: str


class FHIRRiskAssessmentResponse(BaseModel):
    resourceType: Literal["RiskAssessment"]
    status: str
    subject: dict[str, str]
    method: dict[str, str]
    prediction: list[dict[str, Any]]
