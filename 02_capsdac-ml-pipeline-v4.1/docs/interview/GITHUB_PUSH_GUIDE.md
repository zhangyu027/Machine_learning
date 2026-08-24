# GitHub Push Guide

Use this after reviewing the generated package locally.

```bash
cd capsdac-ml-pipeline-master
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make validate
```

If validation passes:

```bash
git status
git add README.md Makefile .github/workflows/ci.yml data/raw data/processed outputs forecasting/src forecasting/scripts docs/interview tests
git commit -m "Improve CAPSDAC interview-ready ML data platform package"
git push origin master
```

If your default branch is `main`, use:

```bash
git push origin main
```

Before interviews, run:

```bash
make validate
uvicorn serving.api.main:app --reload
```
