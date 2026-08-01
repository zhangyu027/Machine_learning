from __future__ import annotations
from pathlib import Path

ALLOWED_SUFFIXES = {".txt", ".md"}

def load_documents(folder: Path) -> list[dict]:
    if not folder.exists():
        raise FileNotFoundError(folder)
    docs=[]
    for path in sorted(folder.rglob("*")):
        if path.is_file() and path.suffix.lower() in ALLOWED_SUFFIXES:
            docs.append({"filename": path.name, "source_path": str(path), "text": path.read_text(encoding="utf-8")})
    return docs

def chunk_documents(documents: list[dict], chunk_size: int=800, overlap: int=120) -> list[dict]:
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Require chunk_size > 0 and 0 <= overlap < chunk_size")
    chunks=[]
    step=chunk_size-overlap
    for doc in documents:
        text=doc["text"]
        for i,start in enumerate(range(0,len(text),step)):
            part=text[start:start+chunk_size].strip()
            if part:
                chunks.append({"filename":doc["filename"],"source_path":doc["source_path"],"chunk_index":i,"text":part,"modality":"document"})
    return chunks
