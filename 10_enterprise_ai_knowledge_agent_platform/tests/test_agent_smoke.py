from pathlib import Path


def test_required_files_exist():
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "README.md",
        root / "build_index.py",
        root / "run_agent.py",
        root / "agents" / "orchestrator.py",
        root / "rag" / "vector_store.py",
        root / "evaluation" / "evaluate_agent.py",
    ]
    missing = [str(path) for path in required if not path.exists()]
    assert not missing, f"Missing required files: {missing}"


def test_vector_store_fallback_imports():
    from rag.vector_store import embed_texts, search_vector_store

    vectors = embed_texts(["healthcare governance", "public sector analytics"], None)
    assert vectors.shape[0] == 2
    assert vectors.shape[1] > 0
    assert callable(search_vector_store)
