from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "siri_rag_requests_total",
    "Total API requests",
    ["route", "status"],
)
REQUEST_LATENCY = Histogram(
    "siri_rag_request_latency_seconds",
    "End-to-end request latency",
    ["route"],
)
RETRIEVAL_LATENCY = Histogram(
    "siri_rag_retrieval_latency_seconds",
    "Vector retrieval latency",
)
GENERATION_LATENCY = Histogram(
    "siri_rag_generation_latency_seconds",
    "LLM generation latency",
)
RETRIEVAL_SCORE = Histogram(
    "siri_rag_top_retrieval_score",
    "Top retrieval similarity score",
)
