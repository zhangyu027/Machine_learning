# Final Check — 09 AI Data Platform Lakehouse

Recommended validation commands:

```bash
pip install -r requirements.txt
python -m scripts.run_pipeline
pytest -q
```

Expected outcome:

- Bronze, Silver, Gold, and Feature Store outputs are generated.
- Quality report and forecast metrics are generated.
- Tests pass.

Notes:

- `pyarrow` is required for parquet read/write.
- The project uses synthetic sample data for portfolio demonstration.
- Do not commit `.venv`, cache folders, or large raw data.
