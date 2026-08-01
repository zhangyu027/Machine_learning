from pathlib import Path
from enterprise_ai_agent.ingestion.documents import load_documents,chunk_documents
from enterprise_ai_agent.rag.vector_store import build_versioned_index
ROOT=Path(__file__).resolve().parents[1]
if __name__=="__main__":
    docs=load_documents(ROOT/"data/sample/documents")+load_documents(ROOT/"data/sample/images")
    active=build_versioned_index(chunk_documents(docs),ROOT/"vector_store/versions")
    print(f"Active index: {active}")
