"""GNN-ready molecular modeling components.

The project exposes a production-style interface while keeping optional heavy
libraries out of the default deploy path. If torch and torch_geometric are
installed, MolecularGNN can be extended into a real message-passing model. In
fallback mode, graph descriptors become deterministic embeddings for demos/tests.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
import numpy as np

from pharma_genai.featurization import graph_features

try:  # pragma: no cover
    import torch
    from torch import nn
    from torch_geometric.nn import GCNConv, global_mean_pool
    TORCH_GEOMETRIC_AVAILABLE = True
except Exception:  # pragma: no cover
    torch = nn = GCNConv = global_mean_pool = None
    TORCH_GEOMETRIC_AVAILABLE = False


@dataclass
class GraphEmbedding:
    smiles: str
    backend: str
    embedding: List[float]
    n_nodes: int
    n_edges: int


class GraphEmbeddingService:
    """Create graph embeddings from molecules using PyG or fallback topology stats."""
    def embed(self, smiles: str) -> GraphEmbedding:
        graph = graph_features(smiles)
        nodes = np.array(graph["node_features"], dtype=float)
        edges = graph["edge_index"]
        if nodes.size == 0:
            emb = np.zeros(8)
        else:
            emb = np.array([
                nodes[:, 0].mean(), nodes[:, 0].std(), nodes[:, 1].mean(), nodes[:, 2].mean(),
                len(nodes), len(edges), max(1, len(edges)) / max(1, len(nodes)), 1.0 if graph["backend"] == "rdkit" else 0.0,
            ], dtype=float)
        emb = np.round(emb / np.maximum(np.abs(emb).max(), 1.0), 4)
        return GraphEmbedding(smiles=smiles, backend=graph["backend"], embedding=emb.tolist(), n_nodes=len(nodes), n_edges=len(edges))


if TORCH_GEOMETRIC_AVAILABLE:  # pragma: no cover
    class MolecularGNN(nn.Module):
        """Minimal PyTorch Geometric GCN for molecular property prediction."""
        def __init__(self, in_channels: int = 4, hidden: int = 64, out_channels: int = 7):
            super().__init__()
            self.conv1 = GCNConv(in_channels, hidden)
            self.conv2 = GCNConv(hidden, hidden)
            self.head = nn.Sequential(nn.Linear(hidden, hidden), nn.ReLU(), nn.Linear(hidden, out_channels), nn.Sigmoid())

        def forward(self, x, edge_index, batch):
            x = self.conv1(x.float(), edge_index).relu()
            x = self.conv2(x, edge_index).relu()
            pooled = global_mean_pool(x, batch)
            return self.head(pooled)
else:
    class MolecularGNN:  # fallback placeholder with explicit behavior
        def __init__(self, *_, **__):
            raise ImportError("Install torch and torch-geometric to train the real MolecularGNN. Use GraphEmbeddingService for fallback embeddings.")
