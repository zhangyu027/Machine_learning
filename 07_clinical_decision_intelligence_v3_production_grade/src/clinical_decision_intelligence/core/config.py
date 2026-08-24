from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Settings:
    model_path: Path
    feedback_path: Path
    api_key: str | None
    rate_limit_per_minute: int
    mlflow_tracking_uri: str
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            model_path=Path(
                os.getenv(
                    "CDI_MODEL_PATH",
                    ROOT / "models/xgboost_readmission_model.joblib",
                )
            ),
            feedback_path=Path(
                os.getenv(
                    "CDI_FEEDBACK_PATH",
                    ROOT / "data/feedback/clinician_feedback.jsonl",
                )
            ),
            api_key=os.getenv("CDI_API_KEY"),
            rate_limit_per_minute=int(os.getenv("CDI_RATE_LIMIT_PER_MINUTE", "60")),
            mlflow_tracking_uri=os.getenv("MLFLOW_TRACKING_URI", str(ROOT / "mlruns")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )


settings = Settings.from_env()
