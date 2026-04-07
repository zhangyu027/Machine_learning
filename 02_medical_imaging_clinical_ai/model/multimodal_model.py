from __future__ import annotations

import torch
import torch.nn as nn

from model.cnn_backbone import CNNClassifier

class MetadataEncoder(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int = 32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

class MultimodalGraphModel(nn.Module):
    def __init__(self, metadata_dim: int, num_classes: int = 2, image_embedding_dim: int = 128, metadata_hidden_dim: int = 32):
        super().__init__()
        self.image_model = CNNClassifier(num_classes=num_classes, embedding_dim=image_embedding_dim)
        self.metadata_encoder = MetadataEncoder(metadata_dim, metadata_hidden_dim)
        fusion_dim = image_embedding_dim + metadata_hidden_dim
        self.fusion = nn.Sequential(
            nn.Linear(fusion_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
        )
        self.classifier = nn.Linear(128, num_classes)

    def forward(self, images: torch.Tensor, metadata: torch.Tensor):
        _, image_embedding = self.image_model(images)
        metadata_embedding = self.metadata_encoder(metadata)
        fused = torch.cat([image_embedding, metadata_embedding], dim=1)
        fused = self.fusion(fused)
        logits = self.classifier(fused)
        return logits, fused
