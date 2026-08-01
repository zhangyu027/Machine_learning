import importlib
from fastapi.testclient import TestClient
def test_health(monkeypatch):
    monkeypatch.setenv("EAK_API_KEY","test-secret")
    import enterprise_ai_agent.config.settings as sm; importlib.reload(sm)
    import enterprise_ai_agent.api.main as main; importlib.reload(main)
    with TestClient(main.app) as client:
        r=client.get('/health'); assert r.status_code==200
        q=client.post('/v1/query',json={'question':'hello'}); assert q.status_code==401
