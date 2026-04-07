from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"

TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"
TEST_DIR = DATA_DIR / "test"
METADATA_DIR = DATA_DIR / "metadata"
METADATA_CSV = Path(os.getenv("METADATA_CSV", METADATA_DIR / "metadata.csv"))

for p in [DATA_DIR, ARTIFACTS_DIR, TRAIN_DIR, VAL_DIR, TEST_DIR, METADATA_DIR]:
    p.mkdir(parents=True, exist_ok=True)

IMAGE_SIZE = int(os.getenv("IMAGE_SIZE", 224))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 8))
EPOCHS = int(os.getenv("EPOCHS", 10))
LR = float(os.getenv("LR", 1e-4))
WEIGHT_DECAY = float(os.getenv("WEIGHT_DECAY", 1e-4))
DEVICE = os.getenv("DEVICE", "cuda")
MODEL_NAME = os.getenv("MODEL_NAME", "resnet18")
MODEL_TYPE = os.getenv("MODEL_TYPE", "multimodal_graph")  # cnn | multimodal_graph
USE_PRETRAINED = os.getenv("USE_PRETRAINED", "false").lower() == "true"

NUM_CLASSES = int(os.getenv("NUM_CLASSES", 2))
METADATA_HIDDEN_DIM = int(os.getenv("METADATA_HIDDEN_DIM", 64))
FUSION_HIDDEN_DIM = int(os.getenv("FUSION_HIDDEN_DIM", 256))
GRAPH_HIDDEN_DIM = int(os.getenv("GRAPH_HIDDEN_DIM", 256))
K_NEIGHBORS = int(os.getenv("K_NEIGHBORS", 4))
GRAPH_ALPHA = float(os.getenv("GRAPH_ALPHA", 0.7))
DROPOUT = float(os.getenv("DROPOUT", 0.2))
NUM_WORKERS = int(os.getenv("NUM_WORKERS", 2))
