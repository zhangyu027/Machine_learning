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
