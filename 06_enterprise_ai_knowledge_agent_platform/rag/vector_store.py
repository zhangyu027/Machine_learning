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
    vectors = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    return np.array(vectors).astype("float32")


def build_vector_store(chunks: List[Dict], output_dir: str, embedding_model_name: str = DEFAULT_EMBEDDING_MODEL):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    model = load_embedding_model(embedding_model_name)
    texts = [chunk["text"] for chunk in chunks]
    vectors = embed_texts(texts, model)

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    faiss.write_index(index, str(output_path / "index.faiss"))
    metadata = {"embedding_model": embedding_model_name, "chunks": chunks}
    (output_path / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return index, metadata


def load_vector_store(index_dir: str):
    index_dir = Path(index_dir)
    index = faiss.read_index(str(index_dir / "index.faiss"))
    metadata = json.loads((index_dir / "metadata.json").read_text(encoding="utf-8"))
    return index, metadata


def search_vector_store(query: str, index_dir: str, top_k: int = 5) -> List[Dict]:
    index, metadata = load_vector_store(index_dir)
    model = load_embedding_model(metadata["embedding_model"])
    query_vector = embed_texts([query], model)
    scores, indices = index.search(query_vector, top_k)

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
