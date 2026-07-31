# Model Card — Scientific ML Drug Discovery Platform V4.1

## Model family
The repository supports classical single-task baselines, a multi-task ADMET demonstration architecture, and an optional molecular GNN architecture.

## Intended use
Research prototyping, reproducible benchmarking, portfolio demonstration, and scientist-facing decision support. Not intended for autonomous compound selection, clinical use, regulatory submission, or replacement of experimental assays.

## Primary scientific claim
No validated superiority claim is currently made. The framework is designed to test whether uncertainty-aware multi-task or graph models improve reliability over classical baselines under scaffold-aware validation.

## Required validation

- Bemis–Murcko scaffold split as primary evaluation
- Random split only as a secondary comparison
- Temporal or external validation when possible
- Endpoint-specific metrics
- Calibration and bootstrap confidence intervals
- Applicability-domain analysis
- Error and subgroup/chemotype analysis
- Reproducible data, code, environment, and model versions

## Outputs

- Endpoint predictions
- Calibration diagnostics
- Uncertainty estimates
- Nearest-training similarity and applicability label
- Transparent priority score
- Explanation artifacts when configured
- Separate literature-evidence packet

## Limitations

- Base installation may use deterministic proxy chemistry when RDKit is absent.
- Existing multi-task outputs include demonstration heuristics unless fitted on a documented endpoint dataset.
- GNN, SHAP, MLflow, and evidence-retrieval capabilities depend on optional dependencies and endpoint-specific validation.
- Applicability-domain thresholds are configurable and require empirical validation.
- Observational or public assay datasets can contain measurement heterogeneity and label noise.

## Human oversight
All outputs are intended for scientist review. Out-of-domain or high-uncertainty molecules should be flagged for review rather than automatically prioritized.
