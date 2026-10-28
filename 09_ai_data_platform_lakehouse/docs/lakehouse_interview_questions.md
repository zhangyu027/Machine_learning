# AI Data Platform / Lakehouse — Interview Preparation

October 28, 2026

1. What did you build?

I built a reproducible synthetic-data lakehouse reference pipeline with Bronze ingestion, Silver cleaning and quality checks, Gold analytical aggregates, an offline feature store, a Random Forest demand forecasting model, and a Streamlit dashboard. I distinguish executable components from design scaffolds.

2. Why Bronze/Silver/Gold?

The layers separate immutable source retention, standardized validated records, and certified business-ready aggregates. This improves traceability, repeatability, and accountability.

3. What did the initial model achieve?

The initial synthetic-data holdout produced MAE 36.35, RMSE 43.61, and R² 0.918 on 85 test rows. I do not present these as real-world operational evidence.

4. What problem did you discover?

Sorting rows by date before a 75/25 split still allowed the boundary month to appear in both training and test sets. I changed the split to operate on unique months with a strict boundary assertion.

5. How did you address leakage?

I used shifted lag and rolling features and replaced contemporaneous record_count with its prior-month lag. The next step is to formalize forecast issue time and audit all feature availability.

6. Why redesign the synthetic label?

The original so-called next-month label was calculated from the same event's inputs. A better demonstration derives labels from later realized monthly demand and tests the true future forecasting task. The revised generator requires end-to-end tests before claiming success.

7. Why not immediately use XGBoost?

Evaluation integrity, appropriate baselines, and realistic labels matter more than algorithm complexity. I first establish reproducible, leakage-aware validation and then compare models.

8. How would you productionize this?

Introduce managed orchestration, transactional lakehouse storage, robust contracts and lineage, privacy/access controls, model registry, monitoring, retraining policies, CI, and operational SLAs. Those are roadmap items, not existing deployed services.

9. What does 100% quality pass rate mean?

Only that all currently implemented checks passed on this synthetic dataset. It does not guarantee semantic validity, freshness, privacy compliance, or completeness of all business rules.

### 10. What would you improve next?

Run rolling-origin backtests, introduce meaningful naive and seasonal baselines, monitor error and bias by county/program, improve synthetic temporal structure, and verify end-to-end pipeline tests.

Suggested closing: The strongest outcome was not just a high R²; it was finding and correcting weaknesses in time-series evaluation and communicating the distinction between demonstration and production readiness.

Repository: https://github.com/zhangyu027/Machine_learning/tree/main/09_ai_data_platform_lakehous

## FINAL INTERVIEW ADDENDUM — OCTOBER 2026

### 11. What did the final model achieve?

On a synthetic 300-prediction holdout, Random Forest achieved MAE ~1.805, RMSE ~2.336, R² ~0.851, and WAPE ~5.65%, compared with last-month baseline MAE ~1.817. That is only ~0.66% lower MAE; I would not claim a reliable ML advantage.

### 12. How did you handle missing future labels?

The last month cannot have an observed next-month target. Summing all-null values had produced a misleading zero point. I updated visualization to drop null targets before aggregation and added a regression test.

### 13. How do you interpret rolling-origin backtests?

Each fold trains on earlier months and evaluates on the next month. I report the number of months where the model beats the baseline and compare average MAE across folds. Results need rerunning before I quote a win rate.

### 14. What does a 100% quality pass rate establish?

Only that nine implemented checks passed; it does not certify source completeness, healthcare validity, or regulatory compliance.

### 15. What is the most credible project takeaway?

The project demonstrates an end-to-end synthetic Bronze/Silver/Gold pipeline, leakage-aware one-month forecasting, honest baselines, and iterative engineering improvements. The model's marginal edge and synthetic assumptions are disclosed rather than overstated.

Final cleanup includes baseline improvement on the Streamlit dashboard, backtest summary, missing-target handling, regression tests, and README limitations. GitHub changes are committed; local test verification is still pending.
