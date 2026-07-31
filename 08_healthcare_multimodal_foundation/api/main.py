from __future__ import annotations

import os
import uuid
from typing import Any, Literal

from fastapi import Depends, FastAPI, Header, HTTPException, status
from prometheus_client import make_asgi_app
from pydantic import BaseModel, Field

from feedback.review import ClinicianReview, FeedbackRepository
from fhir.client import FHIRClient
from observability.telemetry import observe


app = FastAPI(
    title="Healthcare Multimodal Foundation Model API",
    version="2.1.0",
    description=(
        "Synthetic-data portfolio reference API. "
        "Not intended for clinical diagnosis or treatment."
    ),
)

app.mount("/metrics", make_asgi_app())

fhir = FHIRClient()
feedback = FeedbackRepository()


def auth(
    x_api_key: str = Header(default="", alias="X-API-Key"),
) -> None:
    expected = os.getenv("API_KEY")

    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API authentication is not configured",
        )

    if not x_api_key or x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )


class HealthResponse(BaseModel):
    status: Literal["healthy"]
    model: str
    version: str


class PredictRequest(BaseModel):
    patient_id: str = Field(min_length=1)
    structured_features: dict[str, float] = Field(default_factory=dict)
    note: str = Field(default="", max_length=50_000)
    image_embedding: list[float] = Field(default_factory=list)


class PredictResponse(BaseModel):
    prediction_id: str
    risk: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    requires_clinician_review: bool
    fhir_risk_assessment: dict[str, Any]


class ReviewRequest(BaseModel):
    prediction_id: str = Field(min_length=1)
    clinician_id: str = Field(min_length=1)
    decision: Literal["accept", "reject", "override"]
    corrected_label: str | None = None
    comment: str = Field(default="", max_length=2_000)


class ReviewResponse(BaseModel):
    prediction_id: str
    clinician_id: str
    decision: Literal["accept", "reject", "override"]
    corrected_label: str | None = None
    comment: str
    timestamp: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        model="healthcare-mm-v2",
        version=app.version,
    )


@app.post(
    "/v1/predict",
    response_model=PredictResponse,
    dependencies=[Depends(auth)],
)
def predict(req: PredictRequest) -> PredictResponse:
    with observe("predict"):
        completeness = min(
            1.0,
            (
                len(req.structured_features) / 8
                + bool(req.note)
                + bool(req.image_embedding)
            )
            / 3,
        )

        feature_average = (
            sum(req.structured_features.values())
            / max(len(req.structured_features), 1)
        )

        risk = min(
            0.99,
            0.15 + 0.65 * completeness + 0.02 * feature_average,
        )

        prediction_id = str(uuid.uuid4())

        assessment = fhir.create_risk_assessment(
            req.patient_id,
            risk,
            (
                "Multimodal demonstration risk estimate; "
                "clinician validation required."
            ),
            [],
        )

        return PredictResponse(
            prediction_id=prediction_id,
            risk=round(risk, 4),
            confidence=round(completeness, 4),
            requires_clinician_review=True,
            fhir_risk_assessment=assessment,
        )


@app.post(
    "/v1/reviews",
    response_model=ReviewResponse,
    dependencies=[Depends(auth)],
)
def review(req: ReviewRequest) -> ReviewResponse:
    result = feedback.record(
        ClinicianReview(**req.model_dump())
    )
    return ReviewResponse.model_validate(result)
