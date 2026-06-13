# Data Contract Template

## Dataset Name

`<domain>.<dataset_name>`

## Owner

Business Owner:
Technical Owner:
Data Steward:

## Purpose

Describe what this dataset supports.

## Grain

One row represents:

## Schema

| Column | Type | Required | Description | Example |
|---|---|---|---|---|
| id | string | yes | Unique identifier | 123 |

## Quality Rules

| Rule | Severity | Action |
|---|---|---|
| Required fields not null | Critical | Stop pipeline |
| No duplicate grain records | Critical | Stop pipeline |
| Codes must match reference table | High | Alert and quarantine |

## Freshness SLA

Expected update frequency:
Expected availability time:

## Change Management

Breaking changes require:

- PR review
- Business owner approval
- Consumer notification
- Version update
