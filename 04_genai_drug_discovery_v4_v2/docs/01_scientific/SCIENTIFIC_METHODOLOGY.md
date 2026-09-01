# Scientific Methodology — V4.1

## Scientific question

Can uncertainty-aware and representation-rich molecular machine learning improve scaffold-held-out ADMET/toxicity prediction and candidate prioritization compared with simpler endpoint-specific classical baselines?

V4.1 treats this as an empirical question. Model complexity is not assumed to improve generalization.

## Endpoints

The completed benchmark covers four binary endpoints:

- **hERG** — cardiac safety / ion-channel liability.
- **BBBP** — blood-brain barrier penetration.
- **ClinTox** — clinical toxicity benchmark.
- **Tox21** — toxicity task with severe positive-class rarity in the selected task.

All benchmark tables use a normalized `smiles,target` interface.

## Data preparation and integrity

1. Load endpoint-specific labeled molecular data.
2. Remove missing SMILES or target labels.
3. Require binary `0/1` targets.
4. Parse molecular structures with RDKit where required.
5. Audit duplicate structures. Identical SMILES with contradictory labels are excluded from the multi-task training set and recorded rather than silently resolved.
6. Keep benchmark data separate from demonstration inputs.

## Leakage-aware splitting

The primary evaluation uses **Bemis–Murcko scaffold-aware train/validation/test splitting**. Scaffold overlap is explicitly checked. This is intentionally harder than a random molecular split because close structural analogs are less likely to appear on both sides of the train/test boundary.

The frozen endpoint sizes were:

| Endpoint | Train | Validation | Test |
|---|---:|---:|---:|
| hERG | 521 | 65 | 65 |
| BBBP | 1,631 | 204 | 204 |
| ClinTox | 1,184 | 148 | 148 |
| Tox21 | 5,806 | 726 | 726 |

## Label-prevalence audit

Class prevalence was measured overall and within each scaffold partition before interpreting performance.

| Endpoint | Overall positive rate | Train | Validation | Test |
|---|---:|---:|---:|---:|
| hERG | 68.66% | 70.25% | 64.62% | 60.00% |
| BBBP | 76.51% | 77.01% | 75.49% | 73.53% |
| ClinTox | 93.65% | 93.07% | 94.59% | 97.30% |
| Tox21 | 4.24% | 4.84% | 2.34% | 1.38% |

This audit is essential because ClinTox and Tox21 are extremely imbalanced and the scaffold split also introduces prevalence shift.

## Model families

### 1. Classical single-task baselines

- Logistic regression using RDKit molecular descriptors.
- Random forest using 256-bit Morgan fingerprints.

These models are trained separately for each endpoint.

### 2. Multi-task Morgan MLP

A shared neural backbone consumes Morgan fingerprints and produces four endpoint-specific outputs. Missing endpoint labels are handled with a masked binary cross-entropy loss. Endpoint-specific positive-class weights are estimated from training data only.

This experiment tests whether shared representation learning produces positive transfer across endpoints.

### 3. GraphConv GNN

A simple molecular graph baseline uses atom-level features, two GraphConv layers, global mean pooling, dropout, and an endpoint-specific binary classification head. Positive-class weighting and early stopping are used.

The GNN is intentionally a controlled baseline rather than an exhaustive architecture search.

## Evaluation metrics

The benchmark reports:

- ROC-AUC
- Average precision / PR-AUC
- Balanced accuracy
- F1
- Accuracy
- Brier score
- Expected calibration error for the classical benchmark
- Bootstrap 95% confidence intervals for ROC-AUC and average precision in the classical benchmark

For severe imbalance, raw accuracy is not treated as a sufficient performance measure.

## Calibration, applicability domain, and reliability

The classical benchmark adds:

- 10-bin expected calibration error.
- Nearest-training Tanimoto similarity.
- In-domain, borderline, and out-of-domain categories.
- Reliability labels and uncertainty summaries.
- Performance review by applicability-domain group.

This separates ranking performance from probability quality and domain validity.

## Frozen experimental sequence

```text
Endpoint datasets
    ↓
Scaffold-aware split + leakage check
    ↓
Classical baselines
    ↓
Bootstrap CI + calibration
    ↓
Applicability domain + reliability
    ↓
Cross-endpoint comparison
    ↓
Class prevalence / label audit
    ↓
Multi-task Morgan MLP
    ↓
Classical vs multi-task comparison
    ↓
GraphConv GNN
    ↓
All-model comparison
```

The classical scripts were frozen before multi-task and GNN evaluation. The multi-task and GNN baselines were also frozen after their first defined benchmark phase rather than repeatedly tuned against test outcomes.

## Final benchmark interpretation

Across 24 endpoint × metric winner comparisons (six metrics across four endpoints), classical models won 23. Random forest won 13, logistic regression won 10, and the multi-task MLP won one. The GraphConv GNN won none.

The multi-task model's one win was meaningful: **Tox21 average precision improved from 0.2602 for the strongest classical AP baseline to 0.3153**, suggesting possible positive transfer for rare-event retrieval.

The result does not support a claim that more complex models universally improve scaffold-held-out generalization. Instead, it supports endpoint-specific model selection based on prevalence, discrimination, calibration, and domain behavior.

## Reproducibility principle

Only metrics generated by versioned datasets and reproducible scripts should be promoted into the README, report, or interview materials. Test-set results should not be repeatedly optimized after inspection.
