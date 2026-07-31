from __future__ import annotations

import importlib

import pytest
from fastapi.testclient import TestClient

from feedback.review import FeedbackRepository


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch, tmp_path):
    monkeypatch.setenv("API_KEY", "test-secret")

    import api.main as api_main

    importlib.reload(api_main)

    api_main.feedback = FeedbackRepository(
        path=str(tmp_path / "clinician_feedback.jsonl")
    )

    with TestClient(api_main.app) as test_client:
        yield test_client


def auth_headers() -> dict[str, str]:
    return {"X-API-Key": "test-secret"}


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["version"] == "2.1.0"


def test_prediction_requires_authentication(client: TestClient) -> None:
    response = client.post(
        "/v1/predict",
        json={"patient_id": "patient-001"},
    )

    assert response.status_code == 401


def test_prediction_rejects_wrong_key(client: TestClient) -> None:
    response = client.post(
        "/v1/predict",
        headers={"X-API-Key": "wrong-key"},
        json={"patient_id": "patient-001"},
    )

    assert response.status_code == 401


def test_prediction_succeeds(client: TestClient) -> None:
    response = client.post(
        "/v1/predict",
        headers=auth_headers(),
        json={
            "patient_id": "patient-001",
            "structured_features": {
                "age": 65,
                "prior_admissions": 2,
            },
            "note": "Synthetic clinical note.",
            "image_embedding": [0.1, 0.2, 0.3],
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["prediction_id"]
    assert 0.0 <= body["risk"] <= 1.0
    assert 0.0 <= body["confidence"] <= 1.0
    assert body["requires_clinician_review"] is True
    assert "fhir_risk_assessment" in body


@pytest.mark.parametrize(
    "decision",
    ["accept", "reject", "override"],
)
def test_valid_review_decisions(
    client: TestClient,
    decision: str,
) -> None:
    response = client.post(
        "/v1/reviews",
        headers=auth_headers(),
        json={
            "prediction_id": "prediction-001",
            "clinician_id": "clinician-001",
            "decision": decision,
            "comment": "Synthetic test review.",
        },
    )

    assert response.status_code == 200
    assert response.json()["decision"] == decision


def test_invalid_review_decision_returns_422(
    client: TestClient,
) -> None:
    response = client.post(
        "/v1/reviews",
        headers=auth_headers(),
        json={
            "prediction_id": "prediction-001",
            "clinician_id": "clinician-001",
            "decision": "maybe",
        },
    )

    assert response.status_code == 422


def test_openapi_contains_response_models(
    client: TestClient,
) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()
    schemas = schema["components"]["schemas"]

    assert "HealthResponse" in schemas
    assert "PredictResponse" in schemas
    assert "ReviewResponse" in schemas


def test_metrics_endpoint(client: TestClient) -> None:
    response = client.get("/metrics/")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
