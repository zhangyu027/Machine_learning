from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

import numpy as np
import torch
from PIL import Image

from config import cfg
from model.cnn_backbone import CNNClassifier
from model.multimodal_model import MultimodalGraphModel
from model.utils import load_pickle
from preprocessing.dataset import default_transform

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Predictor:
    def __init__(self):
        self.model = self._load_model()
        self.graph_refiner = None
        if cfg.model_type == "multimodal_graph" and cfg.graph_cache_path.exists():
            self.graph_refiner = load_pickle(cfg.graph_cache_path)
        self.transform = default_transform(train=False)

    def _load_model(self):
        if cfg.model_type == "cnn":
            model = CNNClassifier(num_classes=cfg.num_classes)
        else:
            model = MultimodalGraphModel(metadata_dim=len(cfg.metadata_features), num_classes=cfg.num_classes)
        if cfg.model_path.exists():
            model.load_state_dict(torch.load(cfg.model_path, map_location=DEVICE))
        model.to(DEVICE)
        model.eval()
        return model

    def predict(self, image: Image.Image, metadata: Optional[Dict[str, float]] = None):
        image_tensor = self.transform(image).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            if cfg.model_type == "cnn":
                logits, _ = self.model(image_tensor)
                probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
            else:
                metadata = metadata or {}
                metadata_array = np.array([[float(metadata.get(feat, 0.0)) for feat in cfg.metadata_features]], dtype=np.float32)
                metadata_tensor = torch.tensor(metadata_array, dtype=torch.float32, device=DEVICE)
                logits, embedding = self.model(image_tensor, metadata_tensor)
                probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
                if self.graph_refiner is not None:
                    probs = self.graph_refiner.refine(
                        query_embedding=embedding[0].detach().cpu().numpy(),
                        base_probability=probs,
                    )["final_probability"]

        predicted_class = int(np.argmax(probs))
        return {
            "predicted_class": predicted_class,
            "confidence": float(probs[predicted_class]),
            "probabilities": [float(x) for x in probs],
            "class_names": ["negative", "positive"],
        }
