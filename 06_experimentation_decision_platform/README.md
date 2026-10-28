# 06 Experimentation Decision Platform V3

> **Portfolio scope:** This repository uses synthetic data and demonstrates experimentation and causal decision-platform engineering. It is not a live traffic-allocation or production decision system.

A production-oriented reference implementation for converting controlled experiment data into auditable business decisions. It is positioned for Principal Data Engineer, ML Platform, Experimentation Platform, and Applied Scientist interviews.

## Capabilities

- Frequentist A/B analysis with confidence intervals and sample counts
- CUPED variance reduction
- Bayesian Beta-Binomial decision analysis
- Heterogeneous treatment-effect estimation with a T-Learner
- Thompson Sampling simulation
- Reproducible batch artifacts and decision report
- Authenticated FastAPI analysis endpoint and Prometheus metrics
- Automated tests, CI, Docker, typing, linting, dependency audit, and security scan

## Repository structure

```text
api/                    FastAPI service
scripts/                Runnable batch workflows
src/experimentation/    A/B, CUPED, Bayesian, sequential methods
src/causal/             Treatment-effect models
src/bandits/            Adaptive decision simulations
data/raw/               Synthetic source data
tests/                  Unit, API, and pipeline tests
docs/                   Architecture and production-readiness notes
```

Generated outputs under `data/processed/`, `models/`, and `reports/` are intentionally ignored by Git.

## Install and validate

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-all.txt
pytest -q
```

## Run the complete pipeline

Both commands are supported from the project root:

```bash
python -m scripts.run_full_pipeline

# Direct-script execution is also supported:
python scripts/run_full_pipeline.py
```

The pipeline creates a processed dataset, uplift scores, a model artifact, a bandit simulation, and an executive JSON decision report.

## Run the API

```bash
export API_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
uvicorn api.main:app --reload
```

### API endpoints

| Method | Endpoint | Purpose | Authentication |
|---|---|---|---|
| GET | `/health` | Service health and version | No |
| GET | `/metrics/` | Prometheus metrics | No |
| POST | `/v1/analyze/conversion` | Bayesian conversion analysis | API key |

Swagger documentation is available at `http://127.0.0.1:8000/docs`.

## Docker

```bash
export API_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
docker compose up --build
```

## Interview narrative

“I designed an experimentation decision platform that turns governed experiment events into frequentist, variance-reduced, Bayesian, causal, and adaptive decision artifacts. I separated reusable statistical modules from orchestration and API serving, added reproducible outputs and automated quality gates, and documented the path from a local synthetic demonstration to a warehouse-backed enterprise experimentation platform.”

## Responsible positioning

The T-Learner, Bayesian thresholds, and bandit simulator are reference implementations. They have not been validated for production traffic allocation, causal policy decisions, or financial commitments. Enterprise deployment would require a metric catalog, assignment integrity controls, guardrail metrics, sequential-testing policy, model monitoring, privacy controls, and decision governance.


## Installation troubleshooting

Run commands from the repository root—the directory containing `pyproject.toml`.
The supported one-command installation is:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-all.txt
```

This installs the core, API, development, and local editable package dependencies.
If `pandas` or `experimentation` cannot be imported, confirm that the install command
completed successfully and that you are not running from an older Archive copy.

```bash
python -c "import pandas, experimentation; print('environment ready')"
```

### Local validation — 2026-10-28

On macOS with Python 3.10, `python -m pytest -q` returned **16 passed, 1 warning in 1.60s**. The warning was a Starlette TestClient/httpx deprecation warning, not a test failure.

`python -m scripts.run_full_pipeline` completed successfully with 25,000 synthetic observations: revenue uplift **14.0215%**, CUPED-adjusted revenue uplift **13.4275%**, absolute conversion lift **0.04006384** (4.006 percentage points), Bayesian probability of treatment outperforming control **1.0** (100,000 draws), and decision **ship**. These are synthetic example results, not a production decision.

### API key and Swagger quickstart (macOS)

From the project directory, generate a private key and copy it before launching the server:

```bash
export API_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
printf '%s' "$API_KEY" | pbcopy
uvicorn api.main:app --reload
```

Expected: `Uvicorn running on http://127.0.0.1:8000` and `Application startup complete`. Leave the server running. Visit `http://127.0.0.1:8000/docs`, expand **POST /v1/analyze/conversion**, select **Try it out**, paste the clipboard value into **X-API-Key**, provide treatment/control conversions and observations, and click **Execute**. A valid request returns HTTP 200 and a Bayesian analysis response. Swagger does not automatically read the server's environment variable.

To retrieve the key from the **same terminal**, use `printf '%s\\n' "$API_KEY"` (displays a secret) or `printf '%s' "$API_KEY" | pbcopy` (copies it). Stop Uvicorn with Ctrl+C before entering commands in that terminal, then restart it. Another terminal does not automatically inherit the key. Never paste `PASTE_CURRENT_SERVER_KEY_HERE` as the key, publish the secret, or commit it to Git. Rotate exposed keys.

If you see `401 Invalid API key`, verify the Swagger request includes `X-API-Key` and that it matches the server's key. If port 8000 is occupied, inspect `lsof -nP -iTCP:8000 -sTCP:LISTEN` and stop the old Uvicorn server or Docker container. A Swagger **Failed to fetch** message is not an HTTP 200 result; confirm the server is still running.
