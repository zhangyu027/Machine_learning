# Feature Store Layer

Defines reusable feature groups for forecasting:

- enrollment lag features: lag_1, lag_3, lag_6, lag_12
- rolling features: rolling_3, rolling_6
- calendar features: month_sin, month_cos, trend_index
- entity keys: statewide, VendorNumber, PreschoolCDSCode

Production mapping:
- BigQuery feature tables for offline training
- Vertex AI Feature Store or BigQuery serving tables for batch scoring
- feature freshness and null-rate monitoring
