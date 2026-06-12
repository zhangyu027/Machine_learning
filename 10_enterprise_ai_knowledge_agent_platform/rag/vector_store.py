from pathlib import Path
from typing import List, Dict
import json
import math
import re
import numpy as np

try:
    import faiss  # type: ignore
except Exception:  # pragma: no cover - optional dependency fallback
    faiss = None

try:
    from sentence_transformers import SentenceTransformer  # type: ignore
except Exception:  # pragma: no cover - optional dependency fallback
    SentenceTransformer = None

DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
FALLBACK_DIM = 384


def load_embedding_model(model_name: str = DEFAULT_EMBEDDING_MODEL):
    if SentenceTransformer is None:
        return None
    return SentenceTransformer(model_name)


def _hash_embed(text: str, dim: int = FALLBACK_DIM) -> np.ndarray:
    vector = np.zeros(dim, dtype="float32")
    tokens = re.findall(r"[a-zA-Z0-9_]+", text.lower())
    for token in tokens:
        idx = hash(token) % dim
        vector[idx] += 1.0
    norm = np.linalg.norm(vector)
    if norm > 0:
        vector = vector / norm
    return vector.astype("float32")


def embed_texts(texts: List[str], model) -> np.ndarray:
    if model is None:
        return np.vstack([_hash_embed(text) for text in texts]).astype("float32")
    vectors = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    return np.array(vectors).astype("float32")


def build_vector_store(chunks: List[Dict], output_dir: str, embedding_model_name: str = DEFAULT_EMBEDDING_MODEL):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    model = load_embedding_model(embedding_model_name)
    texts = [chunk["text"] for chunk in chunks]
    vectors = embed_texts(texts, model)

    metadata = {
        "embedding_model": embedding_model_name if model is not None else "hash_fallback",
        "chunks": chunks,
        "fallback_dim": int(vectors.shape[1]),
    }
    (output_path / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    # Always save numpy fallback vectors so the project remains runnable without FAISS.
    np.savez_compressed(output_path / "index_fallback.npz", vectors=vectors)

    if faiss is not None:
        index = faiss.IndexFlatIP(vectors.shape[1])
        index.add(vectors)
        faiss.write_index(index, str(output_path / "index.faiss"))
        return index, metadata

    return vectors, metadata


def load_vector_store(index_dir: str):
    index_dir = Path(index_dir)
    metadata = json.loads((index_dir / "metadata.json").read_text(encoding="utf-8"))

    if faiss is not None and (index_dir / "index.faiss").exists():
        index = faiss.read_index(str(index_dir / "index.faiss"))
        return index, metadata

    fallback_path = index_dir / "index_fallback.npz"
    if fallback_path.exists():
        vectors = np.load(fallback_path)["vectors"].astype("float32")
    else:
        # Legacy package fallback: compute vectors from metadata if only metadata.json exists.
        texts = [chunk["text"] for chunk in metadata.get("chunks", [])]
        vectors = embed_texts(texts, None)
    return vectors, metadata


def search_vector_store(query: str, index_dir: str, top_k: int = 5) -> List[Dict]:
    index, metadata = load_vector_store(index_dir)
    chunks = metadata["chunks"]
    model_name = metadata.get("embedding_model", DEFAULT_EMBEDDING_MODEL)
    model = None if model_name == "hash_fallback" else load_embedding_model(model_name)
    query_vector = embed_texts([query], model)

    if faiss is not None and hasattr(index, "search"):
        scores, indices = index.search(query_vector, top_k)
        pairs = list(zip(indices[0], scores[0]))
    else:
        vectors = np.asarray(index).astype("float32")
        scores = vectors @ query_vector[0]
        top_indices = np.argsort(scores)[::-1][:top_k]
        pairs = [(int(idx), float(scores[idx])) for idx in top_indices]

    results = []
    for rank, (idx, score) in enumerate(pairs):
        if idx < 0 or idx >= len(chunks):
            continue
        item = dict(chunks[idx])
        item["score"] = float(score)
        item["rank"] = rank + 1
        results.append(item)
    return results
