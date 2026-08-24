# CAPSDAC ML Pipeline V4 — 12-Month Forecasting & Decision Science

This package updates the prior CAPSDAC V3 forecasting repo for a **realistic 12-month history window**. It is designed for Senior Data Scientist / MLE interviews and separates private CAPSDAC child-level input from portfolio-safe aggregate modeling.

## What changed from V3

- Added a CAPSDAC child-extract adapter that reads the real July 2025–June 2026 schema.
- Uses an explicit allow-list and **never carries child names, addresses, DOB, or child IDs into the modeling table**.
- De-duplicates children within site/month and aggregates to a site-month grain.
- Replaced the V3 3-month / lag-12 default with a **1-month-ahead forecast** that is defensible with exactly 12 months of history.
- Uses `enrollment_t`, lags 1–3, rolling 3-month enrollment, seasonality, program composition, family context, and agency-size features.
- Uses expanding-window monthly validation with four or more temporal holdout folds when 12 months are supplied.
- Removes synthetic capacity/staffing assumptions from the default model outputs.
- Adds an `OperationalReviewFlag` for unusually large forecast changes.
- Keeps champion/challenger selection, drift monitoring, registry, retraining policy, FastAPI, and Streamlit.

## Why the default horizon is 1 month

With only 12 months, a 3-month target plus lag-6/lag-12 features leaves too few independent months for defensible temporal validation. V4 therefore defaults to **H+1**. Once 18–24+ months are available, H+3 and annual-seasonality features can be enabled without sacrificing evaluation quality.

## Private CAPSDAC workflow

Place the real child ZIP outside Git, for example:

```text
data/private/capsdac_jul2025tojun2026_child.csv.zip
```

Then run:

```bash
export PYTHONPATH=$PWD/forecasting:$PWD
python forecasting/scripts/run_capsdac_pipeline.py \
  --child-data data/private/capsdac_jul2025tojun2026_child.csv.zip
```

The adapter reads only approved columns, aggregates to site-month, and deletes the temporary aggregate unless `--keep-private-aggregate` is explicitly set.

## Public demo workflow

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PWD/forecasting:$PWD
python scripts/generate_demo_data.py
pytest
python forecasting/scripts/run_capsdac_pipeline.py
streamlit run dashboards/streamlit_app.py
```

Or:

```bash
./run_pipeline.sh
```

## Modeling grain

```text
Private child extract
        |
        | approved columns only
        v
Child de-duplication within site/month
        |
        v
Site-month aggregate
        |
        +-- enrollment count
        +-- FT share
        +-- IEP share
        +-- DLL share
        +-- homelessness-eligibility share
        +-- median family monthly income
        +-- mean family size
        +-- agency enrollment / active sites
        |
        v
Leakage-safe temporal features
        |
        v
Expanding-window model comparison
        |
        v
Next-month site forecast + operational review flag
```

## Feature set

| Category | Features |
|---|---|
| Enrollment history | `enrollment_t`, `lag_1`, `lag_2`, `lag_3`, `rolling_3` |
| Seasonality | `month_sin`, `month_cos`, `trend_index` |
| Program composition | `ft_share`, `iep_share`, `dll_share`, `homeless_eligibility_share` |
| Family context | `median_family_monthly_income`, `mean_family_size` |
| Agency context | `agency_enrollment`, `agency_active_sites` |

## Candidate models

- Median baseline
- Linear Regression
- Ridge Regression
- Random Forest
- Gradient Boosting
- Extra Trees

The champion is chosen by average expanding-window validation RMSE.

## Interview positioning

**One-line story:**

> I converted a large child-level CAPSDAC reporting extract into a privacy-safer site-month analytical layer, built leakage-safe temporal and program-context features, evaluated multiple forecasting models with expanding-window validation, and operationalized next-month enrollment forecasts through monitoring, registry, API, and dashboard components.

This is stronger than claiming a lag-12 or 3-month forecast from only one year of history because the evaluation design matches the amount of data actually available.

## Privacy and governance

Real CAPSDAC child files are **never included in this repository**. The `.gitignore` excludes `data/private/`, model artifacts, and generated feature files. The public demo generator creates synthetic site-month data only.

## Next upgrade when 18–24+ months are available

Add `lag_6`, `lag_12`, rolling 6/12-month features, direct H+3 targets, year-over-year change, richer site/agency random effects or embeddings, conformal prediction intervals, SHAP explanations, and certification/reconciliation risk scoring.

## V4.1 validation and decision-science upgrade

V4.1 adds three production-oriented improvements:

1. **Calendar-aware drift monitoring.** `month_sin`, `month_cos`, and `trend_index` remain visible diagnostics but are excluded from the operational PSI trigger because deterministic time movement is not population drift.
2. **Rolling monthly backtesting against simple baselines.** The champion is reported beside persistence (`next month = current enrollment`) and rolling-3 baselines. The dashboard shows month-by-month RMSE and improvement versus persistence.
3. **Optional certification reconciliation review.** If agency-level certification and child-count extracts are supplied, V4.1 creates an explainable High/Medium/Low review queue based on count differences. This is deliberately described as a review/rules layer until multiple labeled certification cycles exist; it does not overclaim a trained risk model.

Optional reconciliation run:

```bash
python forecasting/scripts/run_capsdac_pipeline.py \
  --child-data data/private/capsdac_jul2025tojun2026_child.csv.zip \
  --certified-data data/private/certified_enrollment.csv \
  --child-counts-data data/private/child_counts_by_agency.csv
```

### Interview framing

> I designed the system so simple baselines must be beaten under rolling temporal backtests, deterministic calendar movement cannot create false drift alarms, and program-facing reconciliation exceptions are separated from model predictions. That makes the platform useful for both predictive analytics and governed public-sector decision support.
<!-- CAPSDAC V4.1 Forecasting/MLOps: ✅ COMPLETE

Rolling temporal validation: ✅ COMPLETE

Baseline benchmarking: ✅ COMPLETE

Corrected operational drift monitoring: ✅ COMPLETE

Executive Streamlit dashboard: ✅ COMPLETE

Certification/reconciliation framework: ✅ CODE READY

Real certification reconciliation results: ⏳ OPTIONAL / NEXT PHASE -->