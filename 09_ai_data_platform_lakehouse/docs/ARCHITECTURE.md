# Lakehouse Architecture

```text
Raw public-sector / healthcare-style events
        ↓
Streaming simulator
        ↓
Bronze Layer
Raw immutable events
        ↓
Silver Layer
Cleaned, standardized, de-identified records
        ↓
Gold Layer
Certified analytics datasets
        ↓
Feature Store
Reusable ML features
        ↓
MLflow Forecasting Model
        ↓
Dashboard + Governance Report
```

## Layers

### Bronze

Raw immutable data saved as parquet.

### Silver

Cleaned data with standardized schema, missing-value handling, and de-identification-safe fields.

### Gold

Certified business-ready tables for analytics and reporting.

### Feature Store

ML-ready features used by forecasting models.

### Governance Layer

Includes schema checks, quality checks, lineage notes, and privacy guidance.
