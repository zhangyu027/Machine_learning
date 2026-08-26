# V4.1 Reports

This directory contains **frozen scientific benchmark outputs** plus legacy/demo
report artifacts. Files remain at their original paths so the V4.1 experiment
scripts and comparisons remain reproducible.

## Final comparison outputs

- `all_models_endpoint_summary.csv` — endpoint-level winners across classical,
  multi-task, and GraphConv model families.
- `all_models_metric_winners.csv` — winner for every endpoint × metric pair.
- `all_models_overall_win_counts.csv` — aggregate winner counts.
- `all_models_long.csv` — normalized long-form comparison table.

## Classical benchmark

- `herg_benchmark.csv`
- `bbbp_benchmark.csv`
- `clintox_benchmark.csv`
- `tox21_benchmark.csv`
- `cross_endpoint_summary.csv`
- `cross_endpoint_best_models.csv`
- `cross_endpoint_domain_performance.csv`
- `cross_endpoint_reliability.csv`
- `cross_endpoint_reliability_summary.csv`

Endpoint diagnostic folders (`*_details/`) contain calibration tables,
test predictions, applicability-domain performance, and reliability comparisons.

## Label audit

- `endpoint_label_audit.csv`
- `endpoint_label_audit_by_split.csv`

## Multi-task benchmark

- `multitask_admet_metrics.csv`
- `multitask_admet_predictions.csv`
- `multitask_admet_training_history.csv`
- `multitask_conflicting_labels.csv`
- `multitask_vs_classical*.csv`

## GNN benchmark

- `gnn_benchmark.csv`
- `gnn_predictions.csv`
- `gnn_training_history.csv`

## Legacy/demo outputs

`benchmark/`, `tables/`, `figures/`, and `logs/` include earlier demonstration,
visualization, or operational artifacts. They should not be confused with the
frozen V4.1 all-model scientific comparison.

## Final benchmark headline

Across 24 endpoint × metric winner comparisons, classical models won 23:
random forest won 13 and logistic regression won 10. The multi-task Morgan MLP
won one metric: Tox21 average precision (0.3153). The simple GraphConv baseline
won none.

These counts are a compact summary, not a substitute for endpoint-specific
interpretation. ClinTox and Tox21 are severely imbalanced, so raw accuracy and
other threshold-dependent metrics must be read together with prevalence,
balanced accuracy, average precision, Brier score, and domain/calibration evidence.
