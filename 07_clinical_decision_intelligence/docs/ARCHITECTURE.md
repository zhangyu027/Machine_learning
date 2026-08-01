# Architecture

## Executable local architecture

```text
Synthetic encounter data
        ↓
Feature preparation and model training
        ↓
Versioned model bundle
        ↓
FastAPI prediction service
   ↙       ↓        ↘
FHIR   Prometheus   Clinician feedback
```

## Target production architecture

```text
EHR/FHIR + claims + operational sources
                ↓
Governed ingestion and lakehouse layers
                ↓
Validated patient-encounter feature products
                ↓
Offline/online feature store
                ↓
Training orchestration + MLflow registry
                ↓
Secure model-serving API
       ↙            ↓             ↘
Clinical app   Monitoring/drift   Feedback/audit
```

## Design principles

1. Separate synthetic demo behavior from production claims.
2. Require explicit authentication configuration.
3. Use typed contracts for request and response governance.
4. Keep model evaluation, fairness, calibration, and drift visible.
5. Preserve clinician review and auditability.
6. Treat Kubernetes, FHIR, and feature-store components as integration patterns until validated in a real environment.
