# Model Card: CAPSDAC Enrollment Forecast

## Model type
Random Forest Regressor with lag-based and seasonality features.

## Intended use
Aggregate planning for statewide, vendor, and site-level CSPP enrollment demand.

## Not intended for
Individual child eligibility, certified enrollment reporting, or automated funding decisions without official validation.

## Features
lag_1, lag_3, lag_6, lag_12, rolling_3, rolling_6, month_sin, month_cos, trend_index.

## Validation
Holdout period evaluation with MAE, RMSE, and R2. Production validation should include backtesting by vendor/site, drift monitoring, data completeness checks, and domain review.
