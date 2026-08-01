# Final Check

Run:

```bash
pip install -r requirements.txt -r requirements-api.txt -r requirements-dev.txt -e .
python -m scripts.initialize_demo
python -m scripts.build_index
pytest -q
python -m compileall src scripts tests
```

Docker and GitHub Actions must pass before merge to `main`.
