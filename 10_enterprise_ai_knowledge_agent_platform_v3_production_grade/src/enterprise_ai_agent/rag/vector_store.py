from __future__ import annotations
import hashlib, json, os, shutil, tempfile
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from .embeddings import stable_hash_embedding

def _source_hash(chunks: list[dict]) -> str:
    payload="\n".join(f"{c['filename']}:{c['chunk_index']}:{c['text']}" for c in chunks)
    return hashlib.sha256(payload.encode()).hexdigest()

def build_versioned_index(chunks: list[dict], root: Path) -> Path:
    if not chunks:
        raise ValueError("Cannot build an index with no chunks")
    root.mkdir(parents=True, exist_ok=True)
    version=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    candidate=Path(tempfile.mkdtemp(prefix=f"candidate-{version}-", dir=root))
    vectors=np.vstack([stable_hash_embedding(c["text"]) for c in chunks])
    np.savez_compressed(candidate/"index.npz", vectors=vectors)
    manifest={"version":version,"status":"validated","embedding":"stable_sha256_hash_v1","chunk_count":len(chunks),"source_hash":_source_hash(chunks),"built_at":datetime.now(timezone.utc).isoformat(),"chunks":chunks}
    (candidate/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    active=root/"active"
    backup=root/"previous"
    if backup.exists(): shutil.rmtree(backup)
    if active.exists(): active.rename(backup)
    candidate.rename(active)
    return active

def search(query: str, index_dir: Path, top_k: int=5) -> list[dict]:
    if top_k <= 0: raise ValueError("top_k must be positive")
    manifest=json.loads((index_dir/"manifest.json").read_text(encoding="utf-8"))
    vectors=np.load(index_dir/"index.npz")["vectors"].astype("float32")
    q=stable_hash_embedding(query)
    scores=vectors @ q
    idxs=np.argsort(scores)[::-1][:min(top_k,len(scores))]
    results=[]
    for rank,idx in enumerate(idxs,1):
        item=dict(manifest["chunks"][int(idx)])
        item.update(score=float(scores[idx]),rank=rank,index_version=manifest["version"])
        results.append(item)
    return results
