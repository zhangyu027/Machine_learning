import pytest

pytest.importorskip("fastapi")
pytest.importorskip("torchvision")
from fastapi.testclient import TestClient
from api.main import app


def test_health_endpoint():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
