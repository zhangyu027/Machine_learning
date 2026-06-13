# ADR-001: Use Bronze / Silver / Gold Lakehouse Architecture

## Status
Accepted

## Context
Enterprise data platforms need clear separation between raw ingestion, standardized transformation, and business-ready reporting outputs.

## Decision
Use a Bronze / Silver / Gold architecture.

## Rationale
- Bronze preserves source-aligned data.
- Silver applies reusable cleansing, standardization, and business logic.
- Gold provides reporting-ready and AI-ready data products.

## Consequences
- Data lineage is easier to explain.
- Data quality checks can be applied by layer.
- Reporting logic is moved upstream instead of duplicated in dashboards.
