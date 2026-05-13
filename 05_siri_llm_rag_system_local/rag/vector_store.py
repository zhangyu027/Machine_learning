from pathlib import Path
from typing import List, Dict
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def load_embedding_model(model_name: str = DEFAULT_EMBEDDING_MODEL):
    return SentenceTransformer(model_name)


def embed_texts(texts: List[str], model) -> np.ndarray:
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    return np.array(embeddings).astype("float32")


def build_faiss_index(chunks: List[Dict], output_dir: str, embedding_model_name: str = DEFAULT_EMBEDDING_MODEL):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    model = load_embedding_model(embedding_model_name)
    texts = [chunk["text"] for chunk in chunks]

    embeddings = embed_texts(texts, model)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    faiss.write_index(index, str(output_path / "index.faiss"))

    metadata = {
        "embedding_model": embedding_model_name,
        "chunks": chunks,
    }

    (output_path / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return index, metadata


def load_faiss_index(index_dir: str):
    index_path = Path(index_dir) / "index.faiss"
    metadata_path = Path(index_dir) / "metadata.json"

    if not index_path.exists() or not metadata_path.exists():
        raise FileNotFoundError(
            f"Vector store not found in {index_dir}. Run build_index.py first."
        )

    index = faiss.read_index(str(index_path))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    return index, metadata


def search_index(query: str, index_dir: str, top_k: int = 5) -> List[Dict]:
    index, metadata = load_faiss_index(index_dir)
    model = load_embedding_model(metadata["embedding_model"])

    query_embedding = embed_texts([query], model)
    scores, indices = index.search(query_embedding, top_k)

    results = []
    chunks = metadata["chunks"]

    for rank, idx in enumerate(indices[0]):
        if idx < 0 or idx >= len(chunks):
            continue

        item = dict(chunks[idx])
        item["score"] = float(scores[0][rank])
        item["rank"] = rank + 1
        results.append(item)

    return results
