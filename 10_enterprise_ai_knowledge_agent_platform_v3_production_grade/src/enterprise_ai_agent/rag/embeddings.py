from __future__ import annotations
import hashlib, re
import numpy as np

FALLBACK_DIM = 384

def stable_hash_embedding(text: str, dim: int = FALLBACK_DIM) -> np.ndarray:
    if dim <= 0:
        raise ValueError("dim must be positive")
    vector = np.zeros(dim, dtype="float32")
    for token in re.findall(r"[a-zA-Z0-9_]+", text.lower()):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:8], "big") % dim
        vector[idx] += 1.0
    norm = np.linalg.norm(vector)
    return (vector / norm if norm else vector).astype("float32")
