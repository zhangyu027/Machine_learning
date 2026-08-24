# Final Check

## Executed validation

- Python compilation: passed
- Pytest: 12 passed in 1.13 seconds
- Full pipeline: passed
- Production evaluation: passed
- ROC AUC: 0.7434
- Average precision: 0.5619
- Propensity matched ATT: -0.1092 across 18,572 matched pairs

## External merge gates

Before merging, run Docker, Docker Compose, Kubernetes dry-run validation, and GitHub Actions. Do not claim clinical deployment or validation.

## Clean validation commands

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-all.txt
CDI_API_KEY=test-secret pytest -q
python -m scripts.run_full_pipeline
python -m scripts.evaluate_production_readiness
```

## Docker validation

```bash
export CDI_API_KEY=test-secret
docker compose build --no-cache
docker compose up -d
docker compose ps
curl --fail http://127.0.0.1:8000/health
curl --fail http://127.0.0.1:8000/ready
```
