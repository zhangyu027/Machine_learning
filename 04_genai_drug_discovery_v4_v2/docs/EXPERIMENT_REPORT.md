# Experiment Report — Uncertainty-Aware Multi-Task ADMET Benchmark

## Scientific question
Can uncertainty-aware multi-task molecular machine learning improve the reliability of early-stage ADMET candidate prioritization compared with classical single-task baselines?

## Planned comparisons

| Model | Representation | Primary split | Status |
|---|---|---|---|
| Logistic regression | RDKit descriptors | Scaffold | Implemented baseline |
| Random forest | Morgan fingerprint | Scaffold | Implemented baseline |
| XGBoost | RDKit descriptors/fingerprint | Scaffold | Extension |
| Multi-task MLP | Shared molecular representation | Scaffold | Existing architecture; benchmark pending |
| Molecular GNN | Molecular graph | Scaffold | Existing optional architecture; benchmark pending |

## Required endpoint reporting
For every endpoint, record dataset size, class prevalence or target distribution, missing labels, split strategy, preprocessing, model configuration, ROC-AUC/PR-AUC/Brier/ECE or MAE/RMSE, bootstrap confidence intervals, calibration analysis, applicability-domain behavior, and limitations.

## Evidence standard
No result belongs in the main README until it is reproduced from a versioned dataset and saved by the benchmark workflow. Empty benchmark cells must remain empty rather than being populated with aspirational metrics.

## Current status
The V4 upgrade implements the scientific evaluation framework, leakage-aware scaffold splitting, classical baselines, calibration metrics, bootstrap intervals, applicability-domain analysis, transparent candidate ranking, and evidence separation. Full endpoint benchmarks require a selected public dataset and optional RDKit installation.
