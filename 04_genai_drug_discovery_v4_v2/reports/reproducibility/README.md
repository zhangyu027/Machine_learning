# Scientific Benchmark Reproducibility Record

## hERG Benchmark

Status: VALIDATED

Dataset:
- Endpoint: hERG
- Total labeled molecules: 651
- Positive: 447
- Negative: 204

Evaluation:
- Split strategy: Bemis-Murcko scaffold split
- Train: 521
- Validation: 65
- Test: 65
- Random state: 42

Models:
- Logistic Regression with RDKit molecular descriptors
- Random Forest with Morgan fingerprints

Applicability Domain:
- In-domain: 16
- Borderline: 34
- Out-of-domain: 15
- Mean nearest Tanimoto: 0.461378

Reproducibility Validation:
The hERG benchmark was independently rerun in the same software
environment.

The rerun reproduced:
- the same scaffold split
- the same applicability-domain assignments
- identical domain-performance output
- identical reliability-group output
- equivalent benchmark metrics up to machine-level floating-point
  serialization precision

Observed Random Forest differences such as:

    0.1620534587977874
    0.16205345879778738

are numerical serialization differences at approximately 1e-17 and
are not scientifically meaningful.

Conclusion:
The hERG V4.1 scientific benchmark is reproducible within the validated
software environment.

Note:
Historical benchmark values may show small differences when generated
under different dependency versions. These should be treated as
environment/version drift rather than stochastic instability of the
current benchmark.
