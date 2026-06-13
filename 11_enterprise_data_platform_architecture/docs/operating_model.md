# Enterprise Data Platform Operating Model

## Roles

| Role | Responsibility |
|---|---|
| Platform Owner | Defines standards, architecture, and operating model |
| Data Product Owner | Owns business definition and usage expectations |
| Data Engineer | Builds and maintains pipelines |
| Data Steward | Confirms definitions, quality, and governance |
| Security Owner | Reviews access and sensitive data controls |
| Consumer | Uses curated datasets for analytics, reporting, or AI |

## Change Management

All production changes should follow:

```text
Feature Branch
    ↓
Pull Request
    ↓
Technical Review
    ↓
Validation Evidence
    ↓
Deployment
    ↓
Monitoring
```

## Access Model

- Admin: platform support only
- Contributor: assigned developers
- Reader: reviewers and consumers
- Sensitive data access: limited and approved

## Production Readiness Checklist

- Data contract approved
- Quality checks defined
- Lineage captured
- RBAC configured
- Runbook created
- Monitoring enabled
- Cost impact reviewed
- Rollback approach documented
