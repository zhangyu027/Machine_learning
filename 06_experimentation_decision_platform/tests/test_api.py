from __future__ import annotations

import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("API_KEY", "test-secret")
    import api.main as api_main
    importlib.reload(api_main)
    with TestClient(api_main.app) as test_client:
        yield test_client


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "3.0.0"}


def test_analysis_requires_api_key(client: TestClient) -> None:
    response = client.post("/v1/analyze/conversion", json={"treatment": {"conversions": 60, "observations": 100}, "control": {"conversions": 50, "observations": 100}})
    assert response.status_code == 401


def test_conversion_analysis(client: TestClient) -> None:
    response = client.post(
        "/v1/analyze/conversion",
        headers={"X-API-Key": "test-secret"},
        json={"treatment": {"conversions": 60, "observations": 100}, "control": {"conversions": 50, "observations": 100}, "draws": 5_000},
    )
    assert response.status_code == 200
    body = response.json()
    assert 0 <= body["probability_treatment_better"] <= 1
    assert body["recommendation"] in {"ship", "do_not_ship", "continue_experiment"}


def test_invalid_conversion_counts_return_422(client: TestClient) -> None:
    response = client.post(
        "/v1/analyze/conversion",
        headers={"X-API-Key": "test-secret"},
        json={"treatment": {"conversions": 101, "observations": 100}, "control": {"conversions": 50, "observations": 100}},
    )
    assert response.status_code == 422


def test_openapi_has_response_model(client: TestClient) -> None:
    schemas = client.get("/openapi.json").json()["components"]["schemas"]
    assert "ConversionAnalysisResponse" in schemas
