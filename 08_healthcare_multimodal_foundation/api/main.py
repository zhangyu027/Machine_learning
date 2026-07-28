from __future__ import annotations
import os, uuid
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import make_asgi_app
from fhir.client import FHIRClient
from feedback.review import ClinicianReview, FeedbackRepository
from observability.telemetry import observe

app = FastAPI(title="Healthcare Multimodal Foundation Model API", version="2.0.0")
app.mount("/metrics", make_asgi_app())
fhir = FHIRClient(); feedback = FeedbackRepository()

def auth(x_api_key: str = Header(default="")):
    expected = os.getenv("API_KEY", "demo-key")
    if x_api_key != expected: raise HTTPException(401, "Invalid API key")

class PredictRequest(BaseModel):
    patient_id: str
    structured_features: dict[str, float] = Field(default_factory=dict)
    note: str = ""
    image_embedding: list[float] = Field(default_factory=list)

class ReviewRequest(BaseModel):
    prediction_id: str; clinician_id: str; decision: str; corrected_label: str | None = None; comment: str = ""

@app.get("/health")
def health(): return {"status": "healthy", "model": "healthcare-mm-v2"}

@app.post("/v1/predict", dependencies=[Depends(auth)])
def predict(req: PredictRequest):
    with observe("predict"):
        completeness = min(1.0, (len(req.structured_features)/8 + bool(req.note) + bool(req.image_embedding))/3)
        risk = min(.99, .15 + .65*completeness + .02*sum(req.structured_features.values())/max(len(req.structured_features),1))
        prediction_id = str(uuid.uuid4())
        assessment = fhir.create_risk_assessment(req.patient_id, risk, "Multimodal demo risk estimate; clinician validation required.", [])
        return {"prediction_id": prediction_id, "risk": round(risk,4), "confidence": round(completeness,4), "requires_clinician_review": True, "fhir_risk_assessment": assessment}

@app.post("/v1/reviews", dependencies=[Depends(auth)])
def review(req: ReviewRequest):
    return feedback.record(ClinicianReview(**req.model_dump()))
