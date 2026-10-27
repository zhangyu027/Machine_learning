from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="EAK_", env_file=".env", extra="ignore")
    api_key: str | None = None
    enable_ollama: bool = False
    ollama_model: str = "llama3.2"
    ollama_host: str = "http://127.0.0.1:11434"
    index_path: Path = Path("vector_store/active")
    database_path: Path = Path("data/runtime/enterprise_agent.db")
    top_k: int = 5
    chunk_size: int = 800
    chunk_overlap: int = 120
    log_level: str = "INFO"

settings = Settings()
