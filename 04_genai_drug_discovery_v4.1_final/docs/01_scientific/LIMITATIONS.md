# Limitations — V4.1

## Scientific scope

This repository is a portfolio and decision-support research prototype. It is not a validated medicinal-chemistry, clinical, regulatory, or production system. Model outputs are not experimental evidence and must not be used as autonomous compound-selection decisions.

## Dataset limitations

### Small held-out samples

The hERG test set contains only 65 molecules. Confidence intervals are therefore important, and small changes in individual predictions can materially change reported metrics.

### Extreme class imbalance

ClinTox contains 144 positives and only 4 negatives in the held-out test set. Tox21 contains 10 positives and 716 negatives. Raw accuracy, F1, and average precision can be misleading when interpreted without prevalence and class orientation.

For example, a majority-class prediction can achieve very high raw accuracy on Tox21 without useful positive-class retrieval.

### Prevalence shift under scaffold splitting

The scaffold partitions do not preserve identical label prevalence. Tox21 positive prevalence decreases from 4.84% in training to 1.38% in test. This is not automatically a split error: structural families can correlate with activity. However, it makes the test distribution more challenging and complicates direct metric interpretation.

### Assay and label heterogeneity

Public molecular datasets may contain assay heterogeneity, measurement noise, duplicate structures, and contradictory labels. The multi-task workflow excludes identical SMILES with conflicting labels and records the conflict instead of silently choosing one label, but deeper assay harmonization remains future work.

## Modeling limitations

### Classical models remain strongest overall

The completed comparison does not show universal benefit from neural complexity. Classical models won 23 of 24 endpoint × metric comparisons.

This should not be interpreted as proof that classical methods are always superior. It only describes the tested datasets, representations, split protocol, and model configurations.

### Multi-task learning showed limited positive transfer

The shared Morgan MLP did not generally outperform endpoint-specific classical models. Its main positive result was improved Tox21 average precision (0.3153 versus 0.2602 for the strongest classical AP baseline). This may indicate useful transfer for sparse toxicity labels, but it did not generalize across endpoints.

### GNN architecture is intentionally simple

The GraphConv benchmark uses a small two-layer graph network and is not an exhaustive search over message-passing neural networks, graph attention, GIN, directed MPNNs, pretrained molecular encoders, or graph transformers. The GNN winning zero benchmark metrics therefore means only that this defined GraphConv baseline did not outperform the stronger alternatives.

### Limited hyperparameter search

The project prioritizes a reproducible benchmark over aggressive test-driven tuning. More extensive tuning could improve models, but repeatedly adjusting models after reviewing held-out test performance would weaken the validity of the comparison.

## Evaluation limitations

### Metric dependence

There is no single universally correct metric. ROC-AUC, average precision, balanced accuracy, F1, Brier score, and calibration answer different questions. Endpoint selection should reflect the scientific cost of false positives and false negatives.

### Calibration

Expected calibration error is bin-dependent and can be unstable with small samples. Brier score mixes calibration and discrimination. More advanced calibration assessment could include reliability diagrams, calibration slope/intercept, isotonic or Platt calibration, and repeated resampling.

### Applicability domain

The current applicability domain is based on nearest-training Morgan/Tanimoto similarity. It is transparent and useful, but it is only one definition of chemical domain validity. Alternative distance metrics, learned embeddings, conformal methods, and chemotype-specific thresholds may provide complementary evidence.

### Confidence intervals

Bootstrap intervals quantify sampling variability for selected metrics but do not capture all uncertainty sources, including assay noise, dataset construction choices, hyperparameter uncertainty, or domain shift.

## Validation limitations

There is no external or temporal validation set yet. Scaffold-held-out testing is stronger than a simple random split for structural generalization, but it does not replace:

- External datasets from independent sources.
- Temporal validation using later assay data.
- Prospective experimental confirmation.
- Medicinal-chemistry review.
- Clinical or regulatory validation.

## Explainability and evidence limitations

SHAP-ready and literature-retrieval components support interpretation and evidence review, but explanations do not establish causality and retrieved literature does not validate a model prediction.

## Appropriate conclusion

The strongest V4.1 conclusion is not that one architecture is universally best. It is that **model complexity must earn its value under leakage-aware, endpoint-specific evaluation**. In this benchmark, classical models were strongest overall, multi-task learning showed a targeted Tox21 retrieval benefit, and the simple GraphConv baseline did not improve the final comparison.
