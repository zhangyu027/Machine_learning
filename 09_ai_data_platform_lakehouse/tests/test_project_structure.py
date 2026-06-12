from pathlib import Path


def test_required_files_exist():
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "README.md",
        root / "requirements.txt",
        root / "scripts" / "run_pipeline.py",
        root / "src" / "lakehouse_pipeline.py",
        root / "src" / "data_generator.py",
    ]
    missing = [str(path) for path in required if not path.exists()]
    assert not missing, f"Missing required files: {missing}"


def test_requirements_include_parquet_engine():
    root = Path(__file__).resolve().parents[1]
    req = (root / "requirements.txt").read_text().lower()
    assert "pyarrow" in req or "fastparquet" in req
