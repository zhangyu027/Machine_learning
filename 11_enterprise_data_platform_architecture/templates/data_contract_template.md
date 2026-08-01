# Enterprise Data Contract Template

## Dataset identity

- Dataset name:
- Contract version:
- Business owner:
- Technical owner:
- Data steward:
- Consumer groups:

## Purpose and grain

- Business purpose:
- One row represents:
- Primary/business key:

## Delivery expectations

- Update frequency:
- Freshness SLA:
- Availability deadline:
- Source dependency:

## Schema

| Column | Type | Required | Classification | Description | Example |
|---|---|---|---|---|---|
| id | string | yes | internal | Unique identifier | 123 |

## Quality and reconciliation

| Rule | Dimension | Severity | Action | Owner |
|---|---|---|---|---|
| Required fields not null | Completeness | Critical | Stop and quarantine | Technical owner |

## Governance

- Classification:
- Retention period:
- Permitted purposes:
- Access policy:
- Lineage requirements:

## Evolution and compatibility

- Backward-compatibility policy:
- Schema-evolution policy:
- Deprecation window:
- Consumer-notification process:

## Approval history

| Version | Date | Change | Approvers | Status |
|---|---|---|---|---|
