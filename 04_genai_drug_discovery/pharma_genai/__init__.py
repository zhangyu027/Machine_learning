"""Pharma GenAI V2: ADMET, molecular properties, toxicity, reliability, and UI utilities."""
from .pipeline import analyze_smiles, analyze_file
__all__ = ["analyze_smiles", "analyze_file"]
__version__ = "2.0.0"
