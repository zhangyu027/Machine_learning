# Pharmaceutical GenAI Drug Discovery V4.1 Enterprise Platform

## Interview Narrative and Executive Project Report

### Executive summary

Scientific ML Drug Discovery Platform V4.1 is an enterprise-style pharmaceutical AI project designed to support early-stage candidate prioritization. The system accepts molecular inputs, engineers chemistry features, supports benchmark datasets, evaluates scaffold-aware baselines, produces uncertainty-aware candidate decisions, provides feature attribution, retrieves supporting evidence, and exposes deployable app/API patterns.

The project does not claim clinical-grade prediction performance. Its value is to demonstrate a realistic, scientifically responsible architecture for computational drug discovery: predictions are paired with confidence, uncertainty, applicability-domain checks, limitations, and reproducible benchmark workflows.

### Business and scientific problem

Drug discovery teams need to reduce weak candidates early while preserving scientific transparency. Many compounds fail because of ADMET, safety, formulation, or exposure problems rather than lack of target activity. The V4.1 platform addresses this by treating drug discovery as a multi-objective decision-support problem.

### V4.1 upgrade

V4.1 adds a publication-quality scientific benchmarking layer: MoleculeNet-ready dataset workflows, scaffold-aware splitting, descriptor and fingerprint baselines, RDKit-based chemistry handling, stable candidate result schema, GitHub-ready documentation, and a clear evidence policy that prevents invented metrics from being promoted.

### Architecture

The system has six layers: molecular input and validation; molecular representation using descriptors, fingerprints, and graph-ready structures; baseline and multi-task ADMET modeling interfaces; reliability, uncertainty, and applicability-domain assessment; explainability and literature evidence retrieval; and Streamlit, FastAPI, Docker, CI/CD, and MLflow-ready delivery patterns.

### Validation strategy

Software validation includes imports, unit tests, Streamlit smoke tests, benchmark-script execution, and API checks. Scientific validation requires curated labeled datasets, scaffold-aware splits, calibration, applicability-domain review, confidence intervals, external validation, and eventually prospective experimental confirmation.

### Interview summary

I evolved a pharmaceutical AI demo into a scientific ML drug discovery platform. The project demonstrates the full path from molecular input to feature engineering, scaffold-aware benchmarking, uncertainty-aware prioritization, explainability, literature evidence, and deployable MLOps. I intentionally separated demo outputs from scientific performance claims and added benchmark workflows so results can be reproduced and defended.

### Next steps

The next milestones are ClinTox and Tox21 benchmarks, cross-dataset performance tables, ROC/PR curves, calibration plots, hERG curation, calibrated multi-task ADMET training, GNN training, SHAP analysis, and full PubMed/patent retrieval.
# V4.1 Scientific Upgrade Manifest

## Added

- `pharma_genai/data/scaffold_split.py`
- `pharma_genai/models/classical_baselines.py`
- `pharma_genai/evaluation/metrics.py`
- `pharma_genai/evaluation/calibration.py`
- `pharma_genai/evaluation/bootstrap_ci.py`
- `pharma_genai/evaluation/applicability_domain.py`
- `pharma_genai/prioritization/candidate_ranking.py`
- `pharma_genai/evidence/literature_retrieval.py`
- `experiments/run_scientific_benchmark.py`
- `DATA_CARD.md`
- `EXPERIMENT_REPORT.md`
- `reports/benchmark_table.csv`
- `tests/test_scientific_validation.py`

## Updated

- Repositioned README around one scientific question and an evidence-centered lifecycle.
- Updated model card with intended use, validation requirements, limitations, and oversight.
- Updated package version to 4.1.0 and scientific-ML description.

## Validation completed

A direct Python validation run confirmed:

- scaffold groups remain isolated across train/validation/test;
- calibration metrics return valid values;
- applicability-domain similarity and labels execute;
- uncertainty/OOD-aware candidate ranking executes.

The full pytest command did not complete within the container timeout because the environment's optional scientific stack initializes slowly. The newly added validation functions were executed directly and passed. Users should run `python -m pytest -q` in the target conda environment after installation.
