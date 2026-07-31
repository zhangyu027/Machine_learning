# Final Validation Check

## Validation environment

- Validation date: 2026-07-31
- Python runtime used in the review environment: Python 3.13
- Target runtime declared by the project: Python 3.10+
- Input data: synthetic experiment-event CSV

## Evidence collected

The following commands completed successfully:

```bash
python -m compileall -q api scripts src tests
python -m scripts.run_full_pipeline
python -m pytest -q
```

Observed test result:

```text
16 passed
```

The full pipeline completed and produced frequentist, CUPED, Bayesian, uplift-model, bandit, and executive-decision artifacts. Generated artifacts were removed before packaging because they are intentionally excluded by `.gitignore`.

API behavior is covered by automated TestClient tests for health, authentication, conversion analysis, invalid requests, and OpenAPI response schemas.

## Not executed in this review environment

Docker was not available in the packaging environment, so the Docker image and container smoke test could not be executed here. The included GitHub Actions workflow builds and smoke-tests the image after push. Treat a passing container job as a merge requirement.

Ruff, mypy, Bandit, and pip-audit are configured in CI but were not installed in the packaging environment. Their successful GitHub Actions results remain required before merge.

## Merge gate

Merge only after:

- GitHub Actions quality job passes.
- GitHub Actions container job passes.
- No generated artifacts are tracked.
- Documentation matches observed behavior.
- OpenAPI matches the FastAPI implementation.
