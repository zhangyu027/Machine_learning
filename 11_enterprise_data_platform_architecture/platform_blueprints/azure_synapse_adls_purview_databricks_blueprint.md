# Azure Data Platform Blueprint

## Platform Components

| Layer | Azure Component | Purpose |
|---|---|---|
| Storage | ADLS Gen2 | Raw, curated, and reporting data storage |
| Orchestration | ADF / Synapse Pipelines | Scheduling, dependency management, triggers |
| Processing | Synapse Spark / Databricks | PySpark transformations and scalable processing |
| SQL Access | Synapse Serverless SQL | Query parquet/delta outputs for validation and analytics |
| Governance | Microsoft Purview | Catalog, classification, glossary, lineage |
| Security | Azure AD / RBAC / ACLs | Role-based and folder-level access control |
| Secrets | Azure Key Vault | Credential and secret management |
| Observability | Azure Monitor / Log Analytics | Pipeline monitoring, job failures, cost and usage |
| DevOps | Azure DevOps / GitHub | PR review, branching, CI/CD |

## Reference Flow

```text
ADF / Synapse Trigger
    ↓
Parameterized Pipeline
    ↓
Bronze Ingestion
    ↓
Synapse Spark / Databricks Silver Transform
    ↓
Data Quality Validation
    ↓
Gold Business Tables
    ↓
Purview Lineage + Catalog
    ↓
Power BI / APIs / AI Features
```

## Storage Design

Recommended containers:

```text
raw/
bronze/
silver/
gold/
reporting/
metadata/
quality/
archive/
```

Recommended folder convention:

```text
/silver/domain/table_name/ReportMonthKey=YYYYMM/
/gold/subject_area/fact_or_dimension/
/quality/domain/table_name/run_date=YYYY-MM-DD/
```

## Pipeline Parameterization

Core parameters:

```text
Environment
SourceSystem
Domain
TableName
ReportMonthKey
StartDate
EndDate
RunId
OutputPath
```

## Production Controls

- Do not debug production pipelines without authorization.
- Use dev/test/prod environments.
- Use PR review for code changes.
- Use pipeline parameters, not hard-coded paths.
- Capture run metadata for every pipeline execution.
- Store validation results as first-class artifacts.

## Interview Talking Point

> In Azure, I would use ADLS as the governed storage foundation, ADF or Synapse Pipelines for orchestration, Synapse Spark or Databricks for scalable transformation, Purview for catalog and lineage, and Azure DevOps for CI/CD. The goal is to operate the platform safely with traceability, governance, quality checks, and repeatable deployments.
