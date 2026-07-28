"""Prometheus metrics and optional OpenTelemetry spans."""
from __future__ import annotations
from contextlib import contextmanager
from time import perf_counter
try:
    from prometheus_client import Counter, Histogram
    REQUESTS = Counter("healthcare_mm_requests_total", "Requests", ["endpoint", "status"])
    LATENCY = Histogram("healthcare_mm_latency_seconds", "Latency", ["endpoint"])
except ImportError:
    REQUESTS = LATENCY = None

@contextmanager
def observe(endpoint: str):
    start = perf_counter(); status = "success"
    try: yield
    except Exception:
        status = "error"; raise
    finally:
        if REQUESTS: REQUESTS.labels(endpoint, status).inc()
        if LATENCY: LATENCY.labels(endpoint).observe(perf_counter()-start)
