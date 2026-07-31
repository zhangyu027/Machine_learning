"""FastAPI service for experiment decision summaries."""
from __future__ import annotations

import hmac
import os
from typing import Literal

import pandas as pd
from fastapi import Depends, FastAPI, Header, HTTPException, status
from prometheus_client import make_asgi_app
from pydantic import BaseModel, Field

from experimentation.ab_test import difference_in_means
from experimentation.bayesian_ab_test import beta_binomial_ab_test

app = FastAPI(
    title="Experimentation Decision Platform API",
    version="3.0.0",
    description="Portfolio reference API for synthetic experiment analysis.",
)
app.mount("/metrics", make_asgi_app())


def require_api_key(x_api_key: str = Header(default="", alias="X-API-Key")) -> None:
    expected = os.getenv("API_KEY")
    if not expected:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "API authentication is not configured")
    if not x_api_key or not hmac.compare_digest(x_api_key, expected):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid API key")


class HealthResponse(BaseModel):
    status: Literal["healthy"]
    version: str


class ExperimentArm(BaseModel):
    conversions: int = Field(ge=0)
    observations: int = Field(gt=0)


class ConversionAnalysisRequest(BaseModel):
    treatment: ExperimentArm
    control: ExperimentArm
    draws: int = Field(default=20_000, ge=1_000, le=200_000)


class ConversionAnalysisResponse(BaseModel):
    probability_treatment_better: float = Field(ge=0, le=1)
    expected_absolute_lift: float
    credible_interval_95: list[float]
    recommendation: Literal["ship", "do_not_ship", "continue_experiment"]


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="healthy", version=app.version)


@app.post(
    "/v1/analyze/conversion",
    response_model=ConversionAnalysisResponse,
    dependencies=[Depends(require_api_key)],
)
def analyze_conversion(request: ConversionAnalysisRequest) -> ConversionAnalysisResponse:
    if request.treatment.conversions > request.treatment.observations or request.control.conversions > request.control.observations:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Conversions cannot exceed observations")
    result = beta_binomial_ab_test(
        request.treatment.conversions,
        request.treatment.observations,
        request.control.conversions,
        request.control.observations,
        draws=request.draws,
    )
    probability = float(result["prob_treatment_better"])
    lift = float(result["expected_lift"])
    recommendation: Literal["ship", "do_not_ship", "continue_experiment"] = "continue_experiment"
    if probability >= 0.95 and lift > 0:
        recommendation = "ship"
    elif probability <= 0.05 and lift < 0:
        recommendation = "do_not_ship"
    return ConversionAnalysisResponse(
        probability_treatment_better=probability,
        expected_absolute_lift=lift,
        credible_interval_95=list(result["credible_interval_95"]),
        recommendation=recommendation,
    )
