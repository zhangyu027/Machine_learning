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

## Additional local verification — 2026-10-28

User-reported run on macOS with Python 3.10 in the project virtual environment:

```text
python -m pytest -q
16 passed, 1 warning in 1.60s

python -m scripts.run_full_pipeline
"pipeline_status": "completed_successfully"
"observations": 25000
"decision": "ship"
```

The warning was a `StarletteDeprecationWarning` from FastAPI/Starlette TestClient's httpx integration. No tests failed.

Observed synthetic results: revenue relative lift 14.021495119930824%, CUPED-adjusted revenue relative lift 13.427517116167346%, conversion absolute lift 0.04006384025536103 (4.006 percentage points), Bayesian probability treatment better 1.0 (100,000 draws). These are local synthetic demonstration results, not production validation.

The user also reported successful local authenticated Swagger testing. An earlier captured PDF showed the `X-API-Key` header but a `Failed to fetch` response; that PDF is not evidence of an HTTP 200 response.

**Outstanding verification:** Latest GitHub Actions quality and Docker container job results have not been confirmed for the current commit. The 2026-07-31 packaging note above remains historical. Do not mark CI/container checks passed without a completed successful run. Rotate any API key exposed in shared screenshots or chat; no key is stored in this document.
