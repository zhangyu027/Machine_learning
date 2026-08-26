# Scientific ML Drug Discovery Platform V4.1 — Final Executive Interview Narrative

## Executive summary

I evolved a pharmaceutical AI demonstration into a reproducible scientific ML benchmark for early-stage ADMET and toxicity decision support. V4.1 evaluates **hERG, BBBP, ClinTox, and Tox21** using Bemis–Murcko scaffold-aware splits, classical descriptor/fingerprint baselines, calibration and bootstrap confidence intervals, applicability-domain and reliability analysis, a shared multi-task Morgan MLP, and a molecular GraphConv baseline.

The central design principle is: **model complexity must earn its value under held-out evidence rather than being assumed to be better.**

## Final benchmark result

Across **24 endpoint × metric comparisons**, classical models won **23**: random forest won **13**, logistic regression won **10**, the multi-task Morgan MLP won **1**, and the GraphConv GNN won **0**.

The multi-task model's one win is scientifically meaningful: **Tox21 average precision improved to 0.3153 from 0.2602** for the strongest classical AP baseline. This suggests possible positive transfer for rare-positive toxicity retrieval, even though the benefit did not generalize across endpoints.

The GraphConv result was not treated as a failed experiment. It showed that increased architectural complexity did not automatically improve scaffold-held-out generalization.

## Endpoint snapshot

| Endpoint | Best ROC-AUC | Best AP | Best balanced accuracy | Best Brier |
|---|---:|---:|---:|---:|
| hERG | RF 0.8856 | RF 0.9183 | Logistic 0.7949 | Logistic 0.1509 |
| BBBP | Logistic 0.8731 | Logistic 0.9387 | Logistic 0.8367 | RF 0.1290 |
| ClinTox | RF 0.9375 | RF 0.9982* | Logistic 0.8715 | RF 0.0263 |
| Tox21 | Logistic 0.7124 | **Multi-task 0.3153** | RF 0.6472 | RF 0.0143 |

*ClinTox AP must be interpreted with its extreme test prevalence: 144 positives and 4 negatives.*

## Why prevalence matters

ClinTox and Tox21 demonstrate why raw accuracy cannot be the primary scientific story. ClinTox's test set contains **144 positives / 4 negatives**, while Tox21 contains **10 positives / 716 negatives**. Results therefore need balanced accuracy, average precision, Brier score, calibration, confidence intervals, and chemical-domain context.

## Interview positioning

> I built a scientific ML drug-discovery platform to test whether more complex molecular models actually improve scaffold-held-out ADMET performance. I compared descriptor logistic regression, Morgan random forest, a masked multi-task neural network, and a GraphConv GNN across four endpoints. Classical models won 23 of 24 metric comparisons, while multi-task learning improved average precision on the rare-positive Tox21 endpoint. The key lesson was that model selection depends on endpoint prevalence, calibration, chemical domain, and the scientific cost of errors—not architecture novelty.

## Technical depth

- Scaffold splitting for structural generalization.
- Class-prevalence auditing under severe imbalance.
- Masked multi-task loss and training-only class weighting.
- Calibration, bootstrap confidence intervals, and Brier score.
- Nearest-training Tanimoto applicability-domain analysis.
- Reliability and uncertainty-aware review routing.
- Frozen model comparison to avoid test-driven tuning.
- Streamlit, FastAPI, Docker/CI/CD, and MLOps-ready delivery patterns.

## Limitations

V4.1 remains a research and portfolio prototype. It has no independent external or temporal validation, no prospective experimental confirmation, and no medicinal-chemistry, clinical, or regulatory validation. Public assay data can contain label noise and assay heterogeneity. hERG has a small held-out test set. ClinTox and Tox21 are severely imbalanced. The GraphConv architecture is a controlled baseline, not an exhaustive GNN search.

## Next scientific milestones

The next defensible steps are **external/temporal validation**, endpoint-specific error and chemotype analysis, improved probability calibration, and then preregistered evaluation of stronger graph or pretrained molecular representations. Explainability and literature retrieval should continue to support scientist review rather than be presented as model validation.
