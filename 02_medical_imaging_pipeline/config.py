from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"

TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"
TEST_DIR = DATA_DIR / "test"

for p in [DATA_DIR, ARTIFACTS_DIR, TRAIN_DIR, VAL_DIR, TEST_DIR]:
    p.mkdir(parents=True, exist_ok=True)

IMAGE_SIZE = int(os.getenv("IMAGE_SIZE", 224))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 16))
EPOCHS = int(os.getenv("EPOCHS", 10))
LR = float(os.getenv("LR", 1e-4))
NUM_CLASSES = int(os.getenv("NUM_CLASSES", 2))
DEVICE = os.getenv("DEVICE", "cuda")
MODEL_NAME = os.getenv("MODEL_NAME", "resnet18")
