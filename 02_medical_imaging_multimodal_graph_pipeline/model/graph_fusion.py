import torch
from torch import nn

class GraphConvBlock(nn.Module):
    def __init__(self, in_dim: int, out_dim: int, dropout: float = 0.2):
        super().__init__()
        self.linear = nn.Linear(in_dim, out_dim)
        self.norm = nn.LayerNorm(out_dim)
        self.dropout = nn.Dropout(dropout)
        self.use_residual = in_dim == out_dim

    def forward(self, x: torch.Tensor, adjacency: torch.Tensor) -> torch.Tensor:
        h = adjacency @ x
        h = self.linear(h)
        h = self.norm(h)
        h = torch.relu(h)
        h = self.dropout(h)
        if self.use_residual:
            h = h + x
        return h
