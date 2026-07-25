from pathlib import Path
import os
ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = Path(os.getenv("CDI_MODEL_PATH", ROOT / "models/xgboost_readmission_model.joblib"))
API_KEY = os.getenv("CDI_API_KEY", "dev-only-change-me")
RATE_LIMIT_PER_MINUTE = int(os.getenv("CDI_RATE_LIMIT_PER_MINUTE", "60"))
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", str(ROOT / "mlruns"))
