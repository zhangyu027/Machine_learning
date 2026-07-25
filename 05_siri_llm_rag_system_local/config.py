from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("SIRI_RAG_API_KEY", "change-me")
    requests_per_minute: int = int(os.getenv("REQUESTS_PER_MINUTE", "30"))
    index_dir: str = os.getenv("INDEX_DIR", "vector_store")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    enable_otel: bool = os.getenv("ENABLE_OTEL", "false").lower() == "true"


settings = Settings()
