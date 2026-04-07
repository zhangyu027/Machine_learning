from __future__ import annotations

import torch
import torch.nn as nn
from torchvision.models import resnet18

class CNNClassifier(nn.Module):
    def __init__(self, num_classes: int = 2, embedding_dim: int = 128):
        super().__init__()
        backbone = resnet18(weights=None)
        in_features = backbone.fc.in_features
        backbone.fc = nn.Identity()
        self.backbone = backbone
        self.embedding = nn.Sequential(
            nn.Linear(in_features, embedding_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
        )
        self.classifier = nn.Linear(embedding_dim, num_classes)

    def forward(self, images: torch.Tensor):
        features = self.backbone(images)
        embedding = self.embedding(features)
        logits = self.classifier(embedding)
        return logits, embedding
