from enterprise_ai_agent.ingestion.documents import chunk_documents
def test_chunk_validation():
    try: chunk_documents([],100,100)
    except ValueError: pass
    else: raise AssertionError("expected ValueError")
def test_chunks():
    chunks=chunk_documents([{"filename":"a.txt","source_path":"a","text":"abcdef"}],4,1)
    assert len(chunks)>=2
