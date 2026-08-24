# Ingestion Layer

Purpose: land CAPSDAC source snapshots into a governed raw zone.

Production mapping:
- Cloud Storage raw bucket for immutable source snapshots
- BigQuery external or managed tables for query access
- data contracts for schema and privacy validation
- Cloud Composer / Airflow for scheduled ingestion

Public portfolio package includes only de-identified synthetic sample data.
