# Validation Report

## Validation environment

- Package build environment: Linux container
- Python: 3.13
- Test framework: pytest
- Data: synthetic patient encounters supplied with the source package

## Evidence collected

- Python compilation: passed for `src/` and `scripts/`
- Test suite: **12 passed in 1.13 seconds**
- Full training pipeline: passed
- Production evaluation script: passed
- Readmission ROC AUC: **0.7434**
- Readmission average precision: **0.5619**
- Propensity-score matched ATT: **-0.1092** across **18,572** matched pairs
- Typed API tests cover health, readiness, authentication, prediction, FHIR output, feedback, and OpenAPI response schemas

## External gates not executed in this environment

- Docker image build and smoke test
- Docker Compose multi-service validation
- Kubernetes client-side or cluster validation
- GitHub Actions execution

These gates must pass in the target environment before merge.

## Merge gate

Merge only when:

1. All tests pass in a clean Python 3.11 environment.
2. GitHub Actions quality and container jobs pass.
3. Docker health, readiness, prediction, FHIR, feedback, and metrics checks pass.
4. Kubernetes manifests validate.
5. No secrets, generated reports, processed data, caches, or unintended model artifacts are tracked.
6. OpenAPI and documentation match observed API behavior.
