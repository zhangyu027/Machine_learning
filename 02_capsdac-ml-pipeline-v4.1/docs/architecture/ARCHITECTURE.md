# Architecture

## Logical architecture

```text
Secure CAPSDAC extracts
      ↓
Bronze: immutable raw monthly snapshots
      ↓
Silver: validated parquet and data contracts
      ↓
Gold: forecast-ready feature tables and contribution marts
      ↓
ML: recursive Random Forest forecasting
      ↓
Consumption: director report, Streamlit dashboard, CSV/API outputs
```

## Principal-level design decisions

- Use data contracts to prevent schema drift from silently breaking forecasts.
- Partition monthly snapshots by snapshot month and source system.
- Separate site-level model inputs from vendor/statewide reporting outputs.
- Maintain privacy controls by removing child-level PII from the public package.
- Log run metadata, model metrics, and forecast artifacts for reproducibility.
