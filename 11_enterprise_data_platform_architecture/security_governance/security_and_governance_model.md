# Security and Governance Model

## Security principles

- Zero trust and least privilege
- Managed identities and workload federation
- Environment and duty separation
- Private networking by default
- Classification-driven controls
- Auditable and time-bound privileged access
- Encryption at rest and in transit
- Data minimization and purpose limitation

## Control matrix

| Role | Bronze | Silver | Gold | Secrets | Production deployment |
|---|---|---|---|---|---|
| Platform administrator | Support access | Support access | Support access | Admin by exception | Infrastructure only |
| Data engineer | Domain write in dev/test | Domain write | No direct business approval | Read assigned secrets | Through CI/CD |
| Data steward | Read | Read/quality approval | Certification approval | None | None |
| Analyst/consumer | None | Restricted read | Approved read | None | None |
| Security auditor | Audit read | Audit read | Audit read | Audit metadata | Read deployment evidence |

## Required mechanisms

- Microsoft Entra ID groups mapped to Azure RBAC, storage ACLs, and workspace permissions.
- Key Vault with managed-identity access, rotation, and access logging.
- Private endpoints, network segmentation, egress controls, and disabled public access where practical.
- Customer-managed keys for domains requiring enhanced regulatory control.
- Row-level security, column-level security, masking, and tokenization for sensitive products.
- Quarterly access certification and automatic removal of inactive or expired access.
- Break-glass access with approval, expiration, incident ticket, and post-use review.
- Audit-log retention aligned to regulatory and incident-response requirements.

## Governance capabilities

- Purview catalog, glossary, ownership, classification, and lineage
- Data-product certification and deprecation states
- Contract and quality-scorecard linkage
- Retention, legal-hold, and deletion policy
- Responsible AI and feature-use metadata for AI consumers
