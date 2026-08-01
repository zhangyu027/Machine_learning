from __future__ import annotations

import hmac
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, Response, status
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from clinical_decision_intelligence.api.schemas import (
    FeedbackRequest,
    FeedbackResponse,
    FHIRRiskAssessmentResponse,
    HealthResponse,
    PatientFeatures,
    PredictionResponse,
    ReadinessResponse,
    VersionResponse,
)
from clinical_decision_intelligence.core.config import settings
from clinical_decision_intelligence.integrations.feedback import ClinicianFeedbackStore
from clinical_decision_intelligence.integrations.fhir import (
    patient_features_to_fhir_risk_assessment,
)
from clinical_decision_intelligence.ml.predictor import ReadmissionPredictor
from clinical_decision_intelligence.monitoring.metrics import (
    FEEDBACK,
    LATENCY,
    MODEL_LOADED,
    PREDICTION_RISK,
    REQUESTS,
)

SERVICE_VERSION = "3.1.0"
predictor: ReadmissionPredictor | None = None
feedback_store = ClinicianFeedbackStore(settings.feedback_path)
requests_by_key: dict[str, deque[float]] = defaultdict(deque)


@asynccontextmanager
async def lifespan(_: FastAPI):
    global predictor
    predictor = ReadmissionPredictor(settings.model_path)
    MODEL_LOADED.set(1)
    yield
    MODEL_LOADED.set(0)


app = FastAPI(
    title="Clinical Decision Intelligence API",
    version=SERVICE_VERSION,
    description=(
        "Synthetic-data clinical decision-support reference API. "
        "Not a medical device and not for diagnosis or treatment."
    ),
    lifespan=lifespan,
)


def authenticate(x_api_key: str = Header(default="", alias="X-API-Key")) -> None:
    if not settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API authentication is not configured",
        )
    if not x_api_key or not hmac.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    now = time.time()
    queue = requests_by_key[x_api_key]
    while queue and queue[0] < now - 60:
        queue.popleft()
    if len(queue) >= settings.rate_limit_per_minute:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )
    queue.append(now)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="healthy", version=SERVICE_VERSION)


@app.get("/ready", response_model=ReadinessResponse)
def ready() -> ReadinessResponse:
    loaded = predictor is not None
    return ReadinessResponse(status="ready" if loaded else "not_ready", model_loaded=loaded)


@app.get("/version", response_model=VersionResponse)
def version() -> VersionResponse:
    return VersionResponse(service="clinical-decision-intelligence", version=SERVICE_VERSION)


@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


def risk_category(risk: float) -> str:
    return "high" if risk >= 0.7 else "moderate" if risk >= 0.4 else "low"


@app.post(
    "/v1/predict",
    response_model=PredictionResponse,
    dependencies=[Depends(authenticate)],
)
def predict(patient: PatientFeatures) -> PredictionResponse:
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")
    start = time.perf_counter()
    try:
        risk = predictor.predict([patient.model_dump(exclude={"patient_id"})])[0]
        PREDICTION_RISK.observe(risk)
        REQUESTS.labels("predict", "ok").inc()
        return PredictionResponse(
            patient_id=patient.patient_id,
            predicted_readmission_risk=risk,
            risk_category=risk_category(risk),
            model_version=SERVICE_VERSION,
        )
    except ValueError as exc:
        REQUESTS.labels("predict", "validation_error").inc()
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        LATENCY.labels("predict").observe(time.perf_counter() - start)


@app.post(
    "/v1/predict/fhir",
    response_model=FHIRRiskAssessmentResponse,
    dependencies=[Depends(authenticate)],
)
def predict_fhir(patient: PatientFeatures) -> dict:
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")
    risk = predictor.predict([patient.model_dump(exclude={"patient_id"})])[0]
    return patient_features_to_fhir_risk_assessment(
        patient.patient_id,
        risk,
        model_version=SERVICE_VERSION,
    )


@app.post(
    "/v1/feedback",
    response_model=FeedbackResponse,
    dependencies=[Depends(authenticate)],
)
def feedback(item: FeedbackRequest) -> FeedbackResponse:
    decision = "accepted" if item.accepted else "rejected"
    FEEDBACK.labels(decision).inc()
    record = feedback_store.append(item.model_dump())
    return FeedbackResponse.model_validate(record)
