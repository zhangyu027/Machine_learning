# Preferred Azure Physical Architecture

## Reference decision

| Capability | Preferred service | Supported alternative | Decision rationale |
|---|---|---|---|
| Storage | ADLS Gen2 with Delta tables | OneLake | Open lake storage, ACL/RBAC support, broad ecosystem integration |
| Ingestion and orchestration | Azure Data Factory | Databricks Workflows | Strong connector coverage and centralized orchestration |
| Transformation | Azure Databricks | Synapse Spark | Mature Delta Lake, engineering productivity, scalable job compute |
| Governed SQL | Synapse Serverless SQL | Databricks SQL | Low-operations SQL access over curated lake assets |
| Catalog and lineage | Microsoft Purview | Unity Catalog plus Purview integration | Enterprise discovery, classification, glossary, and audit support |
| Secrets | Azure Key Vault | Databricks secret scopes backed by Key Vault | Centralized secret lifecycle and managed-identity access |
| CI/CD | GitHub Actions | Azure DevOps | Repository-integrated validation and environment promotion |
| Monitoring | Azure Monitor and Log Analytics | Databricks system tables | Unified operational telemetry and alerting |

## Environment topology

- Separate Azure subscriptions or resource groups for development, test, and production.
- Private endpoints for storage, Key Vault, SQL, Databricks, and Purview where supported.
- Managed identities for pipelines and workloads; no embedded credentials.
- Separate catalogs/containers and deployment identities per environment.
- Production changes promoted from immutable artifacts after PR and validation approval.
