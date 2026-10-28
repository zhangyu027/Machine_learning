# AI Data Platform / Lakehouse — Technical Findings

October 28, 2026

Context: Synthetic healthcare/public-sector style demand forecasting, not a live operational platform.

Original run: RandomForestRegressor; MAE 36.35, RMSE 43.61, R² 0.918; 255 training and 85 testing observations. Reported train_end and test_start both 2026-02-01.

### Finding 1 — Split integrity: Original chronological holdout split rows after sorting by month, allowing the same calendar month in both sets. Fix: split on unique months and assert strict train/test separation.

### Finding 2 — Feature availability: Original model used current-row record_count while lag/rolling features used shift(1). Fix: replace with record_count_lag1. Still verify all features against a documented forecast issue date.

### Finding 3 — Synthetic target: Original target_next_month_demand was generated from same-row event characteristics rather than independently observed next-month demand. Fix initiated: derive next-month group-level target from next month's realized synthetic demand, allocate across source rows for Gold aggregation. This design still needs full end-to-end validation and a more realistic temporal generator.

### Finding 4 — Evaluation: A strong R² on synthetic data is not proof of real-world performance. Compare against a meaningful lag-based baseline, use rolling-origin backtesting, and report MAE, RMSE, WAPE, bias, and segment performance. Current baseline is provisional and must be reviewed.

### Finding 5 — Visualization: Plot a 45-degree actual-versus-predicted reference, residuals, and error by month/program/county. Present R² separately from MAE/RMSE. Explain what 100% quality-check pass rate measures and what it does not.

### Finding 6 — Architecture: Bronze raw immutable data, Silver standardization and quality checks, Gold certified aggregates, offline feature store, ML forecasting, and dashboard. dbt/Airflow are scaffolds; Spark/Delta/cloud storage are future integrations, not deployed production capabilities.

Validation checklist: rerun pipeline; inspect target and feature dates; run pytest; verify quality gates; inspect metric changes; review new figures; document remaining limitations.

Repository: https://github.com/zhangyu027/Machine_learning/tree/main/09_ai_data_platform_lakehous

## FINAL EVALUATION ADDENDUM — OCTOBER 2026

The revised 60-month synthetic monthly demand process separates observed demand from next-month targets. The latest reported holdout had 300 predictions across 20 county/program series. Random Forest MAE 1.805, RMSE 2.336, R² 0.851, WAPE 5.65%, near-zero bias (~−0.035); previous-month baseline MAE 1.817, or approximately 0.66% MAE improvement. This small gain is not proof of consistent superiority.

All 9 implemented data-quality checks passed, but passing these checks does not prove real-world completeness, accuracy, or regulatory compliance. The Gold chart showed an artificial final zero because the last feature month lacks a future label; cleanup excludes missing targets before plotting. The dashboard now displays baseline improvement and expanding-window backtest win counts and average MAE. Added regression tests for missing-target plotting and backtest-summary consistency. README updated to describe synthetic-data limitations. Code was pushed to GitHub main; final rerun and pytest verification are pending.

Interview framing: emphasize discovery and correction of misleading target construction, strict month-level holdout, properly timed features, transparent baseline comparison, and the difference between a functioning portfolio prototype and validated production forecasting.
