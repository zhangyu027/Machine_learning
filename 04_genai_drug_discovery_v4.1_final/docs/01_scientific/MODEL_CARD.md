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
# V4 Repair Package

This package contains replacement and new files for the uploaded V4 project.
Copy the contents into the root of `04_genai_drug_discovery_v4_v2` while preserving paths.

## Implemented
1. Notebook unpacks all three evaluation return values.
2. Streamlit export is `admet_v4_predictions.csv`.
3. V4 no longer catches all exceptions or delegates to V3.
4. Added one Pydantic result schema.
5. V4 explicitly orchestrates ADMET, graph, explainability, literature, and lookup components.
6. Added RDKit validation/canonicalization/QED/Morgan diversity with explicit no-RDKit fallback.
7. Generator loss ignores padding and reports average epoch loss.
8. Split core, development, ML, and optional requirements.
9. Added output-directory and input-column validation.
10. Added focused tests.

## Important
The complete repository was not uploaded, so this patch assumes the existing modules imported by `pipeline_v4.py` remain at their current paths. Run the commands in `VALIDATION.md` from the repository root.
