# CAPSDAC Level 3 Forecasting Model Card

## Model purpose

Predict 3-month-ahead preschool site enrollment using synthetic CAPSDAC-style monthly snapshots.

## Intended use

Aggregate planning, capacity review, staffing discussion, and early warning analysis.

## Not intended for

Child-level eligibility, certification counts, funding approval, punitive decisions, or automated operational decisions without human review.

## Training target

`TargetEnrollmentH3`: same-site enrollment three months after the feature month.

## Key features

- Enrollment lags: 1, 3, 6, 12 months
- Rolling means: 3, 6, 12 months
- Seasonality: month sine/cosine
- Trend index
- Site capacity
- Lagged capacity utilization
- Lagged attendance rate
- Lagged teacher-student ratio
- County synthetic demographic context

## Validation

Expanding-window monthly validation. Training months always precede validation months.

## Monitoring

Population Stability Index style drift report for features and target. Retraining decision file records whether routine or drift-triggered retraining is recommended.

## Limitations

The public repo uses synthetic data. Metrics should be interpreted as workflow validation, not real-world CAPSDAC performance.
