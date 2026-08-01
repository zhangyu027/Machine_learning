from __future__ import annotations
import hmac
from pathlib import Path
from typing import Literal
from fastapi import Depends, FastAPI, Header, HTTPException, status
from prometheus_client import make_asgi_app
from pydantic import BaseModel, Field
from enterprise_ai_agent.agents.orchestrator import answer_question
from enterprise_ai_agent.config.settings import settings

app=FastAPI(title="Enterprise AI Knowledge Agent API",version="3.0.0",description="Synthetic portfolio reference implementation; retrieved content is untrusted evidence.")
app.mount("/metrics",make_asgi_app())
def require_key(x_api_key:str=Header(default="",alias="X-API-Key"))->None:
    if not settings.api_key: raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE,"API authentication is not configured")
    if not x_api_key or not hmac.compare_digest(x_api_key,settings.api_key): raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Invalid API key")
class HealthResponse(BaseModel): status:Literal["healthy"]; version:str
class QueryRequest(BaseModel): question:str=Field(min_length=2,max_length=5000); top_k:int=Field(default=5,ge=1,le=20)
class QueryResponse(BaseModel): request_id:str; route:str; answer:str; citations:list[str]; confidence:dict; grounding_risk:dict; latency_ms:float; index_version:str|None=None
@app.get("/health",response_model=HealthResponse)
def health()->HealthResponse:return HealthResponse(status="healthy",version=app.version)
@app.get("/ready")
def ready()->dict:
    ok=settings.index_path.exists() and settings.database_path.exists(); return {"ready":ok,"index":str(settings.index_path),"database":str(settings.database_path)}
@app.post("/v1/query",response_model=QueryResponse,dependencies=[Depends(require_key)])
def query(req:QueryRequest)->QueryResponse:
    result=answer_question(req.question,settings.index_path,settings.database_path,req.top_k)
    return QueryResponse.model_validate(result)
