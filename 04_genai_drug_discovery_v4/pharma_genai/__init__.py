"""Pharma GenAI Drug Discovery package."""
try:
    from .pipeline_v3 import analyze_smiles_v3, analyze_many_v3
except Exception:  # keep package importable during partial installs
    analyze_smiles_v3 = analyze_many_v3 = None

__version__ = "3.0.0"
