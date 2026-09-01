# Scientific ML Drug Discovery Platform V4.1 — Executive Interview Narrative

## Executive summary

I evolved a pharmaceutical AI demonstration into a reproducible scientific ML benchmark for early-stage ADMET and toxicity decision support. V4.1 evaluates hERG, BBBP, ClinTox, and Tox21 using leakage-aware Bemis–Murcko scaffold splits, classical descriptor/fingerprint baselines, calibration and confidence intervals, applicability-domain analysis, a shared multi-task neural model, and a molecular GraphConv baseline.

The central design principle is that model complexity must be justified by held-out evidence rather than assumed to be better.

## What I built

The platform connects molecular validation, RDKit descriptors, Morgan fingerprints, molecular graphs, endpoint prediction, calibration, uncertainty/reliability, applicability-domain checks, explainability patterns, literature evidence, Streamlit/FastAPI interfaces, and MLOps-ready delivery.

## Experimental result

Across 24 endpoint × metric comparisons, classical models won 23: random forest won 13 and logistic regression won 10. The multi-task Morgan MLP won one metric, improving Tox21 average precision to 0.3153 versus 0.2602 for the strongest classical AP baseline. The simple GraphConv GNN won no final metrics.

This was not treated as a failed deep-learning experiment. It showed that increased architecture complexity did not automatically improve scaffold-held-out generalization.

## Why the result matters

The prevalence audit revealed that ClinTox and Tox21 require careful interpretation. ClinTox's test set contains 144 positives and 4 negatives; Tox21 contains 10 positives and 716 negatives. Therefore, raw accuracy can be misleading. I used balanced accuracy, average precision, Brier score, calibration, bootstrap confidence intervals, and applicability-domain analysis to interpret performance more responsibly.

## Interview positioning

A concise version:

> I built a scientific ML drug-discovery platform and used it to test whether more complex molecular models actually improved scaffold-held-out ADMET performance. I compared descriptor logistic regression, Morgan random forest, a masked multi-task neural network, and a GraphConv GNN across four endpoints. Classical models won 23 of 24 metric comparisons, while multi-task learning improved average precision on the rare-positive Tox21 endpoint. The key lesson was that model selection depends on endpoint prevalence, calibration, chemical domain, and the scientific cost of errors—not architecture novelty.

## Technical depth

I can discuss:

- Why scaffold splitting is more realistic than random splitting for structural generalization.
- Why ClinTox and Tox21 make raw accuracy misleading.
- How masked loss supports missing labels in multi-task learning.
- Why endpoint-specific class weighting was estimated from training data only.
- How nearest-neighbor Tanimoto similarity supports an applicability-domain signal.
- Why the GNN result was frozen rather than tuned repeatedly against the test set.
- How prediction, uncertainty, evidence retrieval, and scientist review are separated.

## Limitations

The work remains a research prototype. It has no external or temporal validation, no prospective experimental confirmation, and no regulatory or clinical validation. The GraphConv architecture is a baseline rather than an exhaustive GNN search. Public assay data may contain label noise and assay heterogeneity.

## Next scientific milestones

The most defensible next steps are external/temporal validation, endpoint-specific error and chemotype analysis, calibrated probability models, and only then carefully preregistered experiments with stronger molecular architectures or pretrained encoders.
