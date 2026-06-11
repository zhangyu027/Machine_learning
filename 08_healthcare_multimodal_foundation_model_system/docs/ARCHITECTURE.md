# Architecture

## Local Demo Architecture

```text
Synthetic FHIR-style CSVs
    ├── patients
    ├── encounters
    ├── labs
    ├── vitals
    ├── clinical notes
    └── imaging metadata
        ↓
load_sample_sources()
        ↓
build_gold_patient_encounter_table()
        ↓
build_feature_frame()
        ↓
train_model()
        ↓
model metrics + model card
```

## Enterprise Cloud Architecture

```text
Healthcare source systems
    ↓
S3 Raw Zone
    ↓
Glue / EMR Standardization
    ↓
S3 Silver Zone
    ↓
Gold Patient-Encounter Tables
    ↓
Feature Store / SageMaker Training
    ↓
Model Registry + Monitoring
    ↓
Governed Analytics / Clinical AI Applications
```

## Principal DE Design Principles

- Separate raw, silver, and gold data layers.
- Build patient-encounter gold tables as reusable analytical assets.
- Use deterministic feature generation for reproducibility.
- Treat notes and imaging metadata as first-class multimodal inputs.
- Maintain model-card and metrics artifacts for governance.
- Use IaC and CI/CD scaffolding for production readiness.
- Keep PII protection, access controls, lineage, and monitoring central to the design.
