# API Patch Guide

The supplied OpenAPI document exposes `/health`, `/v1/predict`, and `/v1/reviews`, while the README also advertises `/metrics`. Because the current `api/main.py` source was not supplied, this overlay intentionally does not replace it. Apply the following changes to the existing API implementation.

## 1. Add typed response models

```python
from typing import Any, Literal
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: Literal["healthy"] = "healthy"
    version: str

class PredictionResponse(BaseModel):
    prediction_id: str
    patient_id: str
    risk_score: float = Field(ge=0.0, le=1.0)
    risk_label: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: list[dict[str, Any]] = []
    requires_clinician_review: bool

class ReviewResponse(BaseModel):
    review_id: str
    prediction_id: str
    status: Literal["recorded"] = "recorded"
```

Add the matching `response_model=...` argument to each route decorator. Preserve the response fields already returned by your implementation; adjust these models rather than deleting working fields.

## 2. Make authentication behavior explicit

Avoid an optional empty API key in the production contract. A simple pattern is:

```python
import os
from fastapi import Header, HTTPException, status

AUTH_ENABLED = os.getenv("AUTH_ENABLED", "true").lower() == "true"
EXPECTED_API_KEY = os.getenv("API_KEY", "")

def verify_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    if not AUTH_ENABLED:
        return
    if not EXPECTED_API_KEY:
        raise RuntimeError("API_KEY must be configured when AUTH_ENABLED=true")
    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
```

Attach it with `dependencies=[Depends(verify_api_key)]` to protected endpoints. Do not protect `/health` or `/metrics` unless your deployment requires it.

## 3. Add Prometheus metrics endpoint

```python
from fastapi import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

REQUEST_COUNT = Counter(
    "healthcare_mm_requests_total",
    "Total API requests",
    ["method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "healthcare_mm_request_latency_seconds",
    "API request latency",
    ["endpoint"],
)

@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

Instrument requests through middleware or around the endpoint handlers. After implementation, regenerate `openapi.json` and capture a new Swagger screenshot. Note that `include_in_schema=False` intentionally keeps Prometheus output out of Swagger; remove it when you want `/metrics` shown there.

## 4. Add API tests

At minimum, test health, authentication failure/success, prediction validation, review validation, response schemas, and metrics output. `requirements-dev.txt` includes `httpx` for FastAPI `TestClient`.
