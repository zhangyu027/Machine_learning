from __future__ import annotations

import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch, tmp_path):
    monkeypatch.setenv("CDI_API_KEY", "test-secret")
    monkeypatch.setenv("CDI_FEEDBACK_PATH", str(tmp_path / "feedback.jsonl"))

    import clinical_decision_intelligence.core.config as config

    importlib.reload(config)
    import clinical_decision_intelligence.api.app as api_app

    importlib.reload(api_app)
    with TestClient(api_app.app) as test_client:
        yield test_client


def headers() -> dict[str, str]:
    return {"X-API-Key": "test-secret"}


def patient_payload() -> dict:
    return {
        "patient_id": "synthetic-patient-001",
        "age": 72,
        "sex": "F",
        "insurance": "Medicare",
        "hospital_id": "H1",
        "comorbidity_index": 4,
        "prior_admissions_12m": 2,
        "severity_score": 7.5,
        "care_management_program": 1,
        "length_of_stay": 5,
    }


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_readiness(client: TestClient) -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["model_loaded"] is True


def test_auth_required(client: TestClient) -> None:
    response = client.post("/v1/predict", json=patient_payload())
    assert response.status_code == 401


def test_predict(client: TestClient) -> None:
    response = client.post("/v1/predict", headers=headers(), json=patient_payload())
    assert response.status_code == 200
    body = response.json()
    assert 0 <= body["predicted_readmission_risk"] <= 1
    assert body["risk_category"] in {"low", "moderate", "high"}
    assert body["requires_clinician_review"] is True


def test_predict_fhir(client: TestClient) -> None:
    response = client.post("/v1/predict/fhir", headers=headers(), json=patient_payload())
    assert response.status_code == 200
    assert response.json()["resourceType"] == "RiskAssessment"


def test_feedback(client: TestClient) -> None:
    response = client.post(
        "/v1/feedback",
        headers=headers(),
        json={
            "patient_id": "synthetic-patient-001",
            "accepted": True,
            "clinician_id": "synthetic-clinician-001",
            "reason": "Synthetic test feedback",
        },
    )
    assert response.status_code == 200
    assert response.json()["accepted"] is True


def test_openapi_response_models(client: TestClient) -> None:
    schemas = client.get("/openapi.json").json()["components"]["schemas"]
    for name in (
        "HealthResponse",
        "ReadinessResponse",
        "PredictionResponse",
        "FeedbackResponse",
    ):
        assert name in schemas
