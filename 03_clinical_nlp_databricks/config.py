from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "outputs"

for p in [DATA_DIR, MODELS_DIR, OUTPUT_DIR]:
    p.mkdir(parents=True, exist_ok=True)

DATABRICKS_HOST = os.getenv("DATABRICKS_HOST", "")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN", "")
DATABRICKS_CLUSTER_ID = os.getenv("DATABRICKS_CLUSTER_ID", "")

TEXT_COLUMN = "clinical_note"
TARGET_COLUMN = "label"
RANDOM_STATE = 42
MAX_LENGTH = 256
