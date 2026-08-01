try:
    from prometheus_client import Counter, Histogram
    REQUESTS=Counter("eak_requests_total","Agent requests",["route"])
    LATENCY=Histogram("eak_request_latency_seconds","Agent request latency",["route"])
except Exception:
    REQUESTS=LATENCY=None
