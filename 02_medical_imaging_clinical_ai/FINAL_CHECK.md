# Final Check

Validated commands:

```bash
python scripts/run_pipeline.py
pytest -q
```

Expected outputs:

```text
outputs/tables/bronze_imaging_metadata.csv
outputs/tables/silver_imaging_features.csv
outputs/tables/gold_patient_imaging_features.csv
outputs/tables/evaluation_metrics.csv
evaluation/evaluation_summary.json
models/baseline_imaging_model.json
```

Portfolio status: ready for Data Engineer / Principal Data Engineer interview use.
