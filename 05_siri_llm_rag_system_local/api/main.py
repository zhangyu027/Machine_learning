from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.responses import Response, StreamingResponse
from pydantic import BaseModel, Field
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from config import settings
from observability.logging_config import configure_logging
from observability.metrics import (
    GENERATION_LATENCY,
    REQUEST_COUNT,
    REQUEST_LATENCY,
    RETRIEVAL_LATENCY,
    RETRIEVAL_SCORE,
)
from observability.tracing import configure_tracing, span
from rag.ollama_client import ask_ollama, stream_ollama
from rag.vector_store import search_index
from security.rate_limit import InMemoryRateLimiter

configure_logging(settings.log_level)
logger = logging.getLogger("siri-rag-api")
app = FastAPI(title="Siri Local LLM RAG API", version="2.0.0")
configure_tracing(app, settings.enable_otel)
rate_limiter = InMemoryRateLimiter(settings.requests_per_minute)


class QueryRequest(BaseModel):
    question: str = Field(min_length=2, max_length=4000)
    top_k: int = Field(default=5, ge=1, le=20)
    model: str | None = None


class Source(BaseModel):
    rank: int
    filename: str
    chunk_index: int
    score: float
    text: str


class QueryResponse(BaseModel):
    request_id: str
    answer: str
    sources: list[Source]
    latency_ms: float


def require_api_key(x_api_key: str = Header(default="")) -> None:
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    client = request.client.host if request.client else "unknown"
    if not rate_limiter.allow(client):
        REQUEST_COUNT.labels(route=request.url.path, status="429").inc()
        return Response(
            content=json.dumps({"detail": "Rate limit exceeded", "request_id": request_id}),
            status_code=429,
            media_type="application/json",
        )

    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Unhandled request failure", extra={"request_id": request_id, "route": request.url.path})
        raise
    latency_ms = (time.perf_counter() - start) * 1000
    response.headers["x-request-id"] = request_id
    REQUEST_COUNT.labels(route=request.url.path, status=str(response.status_code)).inc()
    REQUEST_LATENCY.labels(route=request.url.path).observe(latency_ms / 1000)
    logger.info(
        "request_complete",
        extra={
            "request_id": request_id,
            "route": request.url.path,
            "latency_ms": round(latency_ms, 2),
            "status_code": response.status_code,
        },
    )
    return response


@app.get("/health")
def health():
    index_ok = (Path(settings.index_dir) / "index.faiss").exists()
    return {"status": "ok", "index_ready": index_ok, "model": settings.ollama_model}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


async def retrieve(question: str, top_k: int):
    start = time.perf_counter()
    with span("retrieval"):
        results = await asyncio.to_thread(search_index, question, settings.index_dir, top_k)
    RETRIEVAL_LATENCY.observe(time.perf_counter() - start)
    if results:
        RETRIEVAL_SCORE.observe(results[0]["score"])
    return results


@app.post("/v1/query", response_model=QueryResponse, dependencies=[Depends(require_api_key)])
async def query(payload: QueryRequest, request: Request):
    started = time.perf_counter()
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    results = await retrieve(payload.question, payload.top_k)
    if not results:
        raise HTTPException(status_code=404, detail="No indexed context found")

    generation_start = time.perf_counter()
    with span("generation"):
        answer = await asyncio.to_thread(
            ask_ollama,
            payload.question,
            results,
            payload.model or settings.ollama_model,
        )
    GENERATION_LATENCY.observe(time.perf_counter() - generation_start)
    return QueryResponse(
        request_id=request_id,
        answer=answer,
        sources=[Source(**item) for item in results],
        latency_ms=round((time.perf_counter() - started) * 1000, 2),
    )


@app.post("/v1/query/stream", dependencies=[Depends(require_api_key)])
async def query_stream(payload: QueryRequest):
    results = await retrieve(payload.question, payload.top_k)
    if not results:
        raise HTTPException(status_code=404, detail="No indexed context found")

    def event_stream():
        yield f"event: sources\ndata: {json.dumps(results)}\n\n"
        for token in stream_ollama(payload.question, results, payload.model or settings.ollama_model):
            yield f"event: token\ndata: {json.dumps({'text': token})}\n\n"
        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
