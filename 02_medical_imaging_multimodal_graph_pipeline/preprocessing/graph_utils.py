import torch
import torch.nn.functional as F

def build_batch_graph(image_features: torch.Tensor,
                      metadata_features: torch.Tensor,
                      k_neighbors: int = 4,
                      alpha: float = 0.7) -> torch.Tensor:
    """
    Build a symmetric normalized adjacency matrix from image and metadata features.
    Graph is built per mini-batch so the code stays dependency-light (pure PyTorch).
    """
    batch_size = image_features.size(0)
    if batch_size == 1:
        return torch.eye(1, device=image_features.device)

    image_features = F.normalize(image_features, dim=1)
    if metadata_features is not None and metadata_features.size(1) > 0:
        metadata_features = F.normalize(metadata_features, dim=1)
        fused = torch.cat([alpha * image_features, (1 - alpha) * metadata_features], dim=1)
    else:
        fused = image_features

    sim = fused @ fused.t()
    sim.fill_diagonal_(1.0)

    k = min(k_neighbors + 1, batch_size)
    topk_idx = torch.topk(sim, k=k, dim=1).indices

    adjacency = torch.zeros_like(sim)
    adjacency.scatter_(1, topk_idx, 1.0)

    adjacency = torch.maximum(adjacency, adjacency.t())
    adjacency.fill_diagonal_(1.0)

    degree = adjacency.sum(dim=1)
    degree_inv_sqrt = torch.pow(degree.clamp(min=1.0), -0.5)
    norm_adj = degree_inv_sqrt.unsqueeze(1) * adjacency * degree_inv_sqrt.unsqueeze(0)
    return norm_adj
