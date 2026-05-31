# Portfolio Project Brief: Pharmaceutical GenAI Drug Discovery V2

## Objective
Build a portfolio-ready pharmaceutical machine learning package that combines generative drug-discovery outputs with ADMET prediction, toxicity screening, molecular feature engineering, and uncertainty-aware reliability scoring.

## Pharmaceutical ML Capabilities
- RDKit-first molecular descriptor engineering with a fallback parser for lightweight demos.
- Molecular property prediction: molecular weight, LogP, TPSA, HBD/HBA, rotatable bonds, ring counts, QED, fraction CSP3.
- ADMET prediction: oral absorption, solubility risk, BBB penetration, CYP inhibition risk.
- Toxicity prediction: hERG, hepatotoxicity, AMES-like mutagenicity proxy, and combined toxicity risk.
- Wenkel Liang-style reliability scoring: ensemble-proxy disagreement, applicability domain, uncertainty score, and beta-binomial style confidence communication.
- Streamlit UI for interactive portfolio demonstration.

## Why this is pharmaceutical-grade for portfolio use
This project does not claim to replace validated commercial tools. It demonstrates the architecture expected in a real pharmaceutical ML workflow: feature engineering, model scoring, reliability estimation, ranking, explainable notes, reproducible CLI, tests, and UI.

## Suggested next upgrade
Train/calibrate the scoring layer with real labels from TDC, ChEMBL, Tox21, ClinTox, or ADMETlab and replace rules with validated ensemble learners.
