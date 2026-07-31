# Architecture

## Scope and status legend

- **Executable locally:** included in the portfolio demo and expected to run without external cloud services.
- **Implemented scaffold:** code or configuration that demonstrates the production pattern but is not connected to a live healthcare environment.
- **Production integration path:** an intended enterprise extension, not a claim of deployment.

## Local executable architecture

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

The local baseline validates ingestion, joining, feature generation, model training, and governance-artifact creation. It is not intended to establish clinical performance.

## V2 application architecture

```text
FHIR/EHR + Clinical Notes + Imaging Metadata
                   ↓
          Lakehouse / Feature Store
                   ↓
Vision Encoder + Text Encoder + Structured Encoder
                   ↓
           Multimodal Fusion Layer
                   ↓
 Risk Score + Multimodal Embedding Index
                   ↓
 Clinical RAG + Evidence Validation
                   ↓
FHIR RiskAssessment + Clinician Review
                   ↓
 MLflow + Prometheus/OpenTelemetry
                   ↓
      Docker / Kubernetes / GPU Serving
```

### Current executable demonstrations

- Synthetic multimodal source loading and patient-encounter gold-table construction
- Deterministic feature engineering and baseline model training
- Model metrics and model-card artifacts
- Local multimodal fusion and in-memory retrieval interfaces
- FastAPI health, prediction, and clinician-review endpoints
- Retrieval and grounded-generation evaluation metrics

### Implemented scaffolds

- AWS Glue, SageMaker, Step Functions, Terraform, and CI/CD patterns
- MLflow integration with an offline JSON fallback
- Prometheus/OpenTelemetry dependency and instrumentation path
- Docker/Kubernetes/GPU resource definitions

### Production integration paths

- External FHIR servers and DICOM systems
- Production vector databases such as FAISS or Milvus services
- Feast or an equivalent managed feature store
- Distributed PyTorch, DeepSpeed, or Ray training
- Live hospital deployment and clinical validation

## Enterprise cloud architecture

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

## Principal Data Engineering design principles

- Separate raw, silver, and gold data layers.
- Build patient-encounter gold tables as reusable analytical assets.
- Use deterministic feature generation for reproducibility.
- Treat notes and imaging metadata as first-class multimodal inputs.
- Maintain model-card and metrics artifacts for governance.
- Use infrastructure as code and CI/CD scaffolding for production readiness.
- Keep PII protection, access controls, lineage, and monitoring central to the design.
- Clearly distinguish executable demonstrations from future integrations.
