"""Pharma GenAI Drug Discovery V4.1.

Scientific ML research and decision-support toolkit for scaffold-aware
ADMET/toxicity benchmarking, uncertainty, applicability-domain analysis,
multi-task learning, molecular graph modeling, and evidence-supported
candidate prioritization.

The legacy ``analyze_smiles_v3`` / ``analyze_many_v3`` exports are retained
for backward compatibility with the demonstration application layer.
"""

try:
    from .pipeline_v3 import analyze_smiles_v3, analyze_many_v3
except Exception:  # keep package importable during partial installs
    analyze_smiles_v3 = analyze_many_v3 = None

__version__ = "4.1.0"
