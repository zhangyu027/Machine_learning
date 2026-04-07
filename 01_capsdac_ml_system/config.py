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

SYNAPSE_SERVER = os.getenv("SYNAPSE_SERVER", "")
SYNAPSE_DATABASE = os.getenv("SYNAPSE_DATABASE", "")
SYNAPSE_USERNAME = os.getenv("SYNAPSE_USERNAME", "")
SYNAPSE_PASSWORD = os.getenv("SYNAPSE_PASSWORD", "")

TARGET_COLUMN = "enrollment_flag"
RANDOM_STATE = 42
