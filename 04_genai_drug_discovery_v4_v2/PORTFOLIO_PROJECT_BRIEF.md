# Portfolio Project Brief: Scientific ML Drug Discovery Platform V4.1

## Objective

Build a GitHub- and interview-ready pharmaceutical machine-learning platform that combines molecular feature engineering, scaffold-aware benchmarking, ADMET decision support, uncertainty-aware candidate ranking, explainability, evidence retrieval, and deployable software interfaces.

## Core capabilities

- RDKit-first SMILES validation, canonicalization, descriptor engineering, QED, and fingerprint support.
- Scaffold-aware benchmarking using Bemis-Murcko scaffolds when RDKit is available.
- Classical baselines using descriptor logistic regression and Morgan-fingerprint random forest.
- ADMET and toxicity decision-support schema with candidate ranking.
- Reliability scoring through confidence, uncertainty, and applicability-domain style outputs.
- Explainability through feature-attribution outputs and SHAP-ready design.
- PubMed-style literature retrieval pattern for scientist review.
- Streamlit UI, FastAPI-ready service pattern, Docker/MLflow/CI architecture.

## Current benchmark status

- BBBP can be downloaded from DeepChem MoleculeNet and used as the first labeled benchmark.
- ClinTox and Tox21 are recommended next.
- hERG should be added later from TDC or a carefully curated ChEMBL-derived dataset.

## Interview value

The project demonstrates practical skills in cheminformatics, machine learning, MLOps, application development, reproducible benchmarking, scientific communication, uncertainty estimation, and responsible AI decision support.
