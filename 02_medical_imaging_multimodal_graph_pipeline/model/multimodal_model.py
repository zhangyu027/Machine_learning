from typing import Optional

import torch
from torch import nn

from config import (
    MODEL_TYPE, METADATA_HIDDEN_DIM, GRAPH_HIDDEN_DIM,
    K_NEIGHBORS, GRAPH_ALPHA, DROPOUT
)
from model.cnn_backbone import CNNBackbone
from model.graph_fusion import GraphConvBlock
from preprocessing.graph_utils import build_batch_graph

class MultiModalGraphClassifier(nn.Module):
    def __init__(self,
                 num_classes: int,
                 metadata_dim: int,
                 model_type: str = MODEL_TYPE,
                 k_neighbors: int = K_NEIGHBORS,
                 graph_alpha: float = GRAPH_ALPHA,
                 dropout: float = DROPOUT):
        super().__init__()
        self.model_type = model_type
        self.metadata_dim = metadata_dim
        self.k_neighbors = k_neighbors
        self.graph_alpha = graph_alpha

        self.cnn = CNNBackbone()
        image_dim = self.cnn.output_dim

        if metadata_dim > 0:
            self.metadata_encoder = nn.Sequential(
                nn.Linear(metadata_dim, METADATA_HIDDEN_DIM),
                nn.ReLU(),
                nn.Dropout(dropout),
            )
            metadata_out_dim = METADATA_HIDDEN_DIM
        else:
            self.metadata_encoder = None
            metadata_out_dim = 0

        if self.model_type == "cnn":
            self.classifier = nn.Linear(image_dim, num_classes)
        elif self.model_type == "multimodal_graph":
            fused_dim = image_dim + metadata_out_dim
            self.pre_graph = nn.Sequential(
                nn.Linear(fused_dim, GRAPH_HIDDEN_DIM),
                nn.ReLU(),
                nn.Dropout(dropout),
            )
            self.gnn1 = GraphConvBlock(GRAPH_HIDDEN_DIM, GRAPH_HIDDEN_DIM, dropout=dropout)
            self.gnn2 = GraphConvBlock(GRAPH_HIDDEN_DIM, GRAPH_HIDDEN_DIM, dropout=dropout)
            self.classifier = nn.Linear(GRAPH_HIDDEN_DIM, num_classes)
        else:
            raise ValueError(f"Unsupported MODEL_TYPE={self.model_type}")

    def encode_metadata(self, metadata: Optional[torch.Tensor], batch_size: int, device) -> torch.Tensor:
        if self.metadata_encoder is None:
            return torch.zeros(batch_size, 0, device=device)
        if metadata is None or metadata.numel() == 0:
            metadata = torch.zeros(batch_size, self.metadata_dim, device=device)
        return self.metadata_encoder(metadata)

    def forward(self, images: torch.Tensor, metadata: Optional[torch.Tensor] = None) -> torch.Tensor:
        image_features = self.cnn(images)

        if self.model_type == "cnn":
            return self.classifier(image_features)

        batch_size = images.size(0)
        metadata_features = self.encode_metadata(metadata, batch_size=batch_size, device=images.device)
        fused = torch.cat([image_features, metadata_features], dim=1)
        fused = self.pre_graph(fused)

        adjacency = build_batch_graph(
            image_features.detach(),
            metadata_features.detach() if metadata_features.size(1) > 0 else None,
            k_neighbors=self.k_neighbors,
            alpha=self.graph_alpha,
        )

        x = self.gnn1(fused, adjacency)
        x = self.gnn2(x, adjacency)
        logits = self.classifier(x)
        return logits
