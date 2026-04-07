import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

@dataclass
class Config:
    project_root: Path = Path(__file__).resolve().parent
    data_dir: Path = project_root / "data"
    artifacts_dir: Path = project_root / "artifacts"
    train_dir: Path = data_dir / "train"
    val_dir: Path = data_dir / "val"
    test_dir: Path = data_dir / "test"

    metadata_csv: Path = data_dir / "metadata.csv"
    image_size: int = int(os.getenv("IMAGE_SIZE", "224"))
    batch_size: int = int(os.getenv("BATCH_SIZE", "8"))
    epochs: int = int(os.getenv("EPOCHS", "3"))
    learning_rate: float = float(os.getenv("LEARNING_RATE", "1e-3"))
    model_type: str = os.getenv("MODEL_TYPE", "cnn")  # cnn | multimodal_graph
    num_classes: int = 2
    metadata_features: List[str] = field(default_factory=lambda: [
        "age", "sex_binary", "bmi", "lab_crp"
    ])
    model_path: Path = artifacts_dir / "model.pt"
    scaler_path: Path = artifacts_dir / "metadata_scaler.pkl"
    graph_cache_path: Path = artifacts_dir / "graph_cache.pkl"
    blend_alpha: float = float(os.getenv("BLEND_ALPHA", "0.7"))
    knn_k: int = int(os.getenv("KNN_K", "5"))

cfg = Config()
cfg.artifacts_dir.mkdir(parents=True, exist_ok=True)
