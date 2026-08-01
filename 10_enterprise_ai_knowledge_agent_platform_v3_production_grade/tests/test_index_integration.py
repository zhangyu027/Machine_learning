from pathlib import Path
from enterprise_ai_agent.rag.vector_store import build_versioned_index,search
def test_index(tmp_path:Path):
    chunks=[{"filename":"a.txt","source_path":"a","chunk_index":0,"text":"healthcare governance controls","modality":"document"}]
    active=build_versioned_index(chunks,tmp_path)
    result=search("governance",active,1)
    assert result[0]["filename"]=="a.txt"
