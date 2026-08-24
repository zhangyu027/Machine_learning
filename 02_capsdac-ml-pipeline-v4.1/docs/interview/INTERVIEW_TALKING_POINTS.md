# Interview Talking Points

## 60-second summary

I upgraded a CAPSDAC enrollment forecasting workflow into a production-style education data platform. The project ingests de-identified monthly enrollment snapshots, validates data contracts, builds lag and seasonality features, trains a random forest model, recursively forecasts future enrollment, and produces vendor/site/statewide planning outputs. I also designed the AWS production path with S3 lakehouse layers, Glue, Step Functions, SageMaker, Athena, CloudWatch, IAM, and CI/CD.

## Principal-level signals

- I separated source ingestion, feature engineering, modeling, and reporting into maintainable modules.
- I added data contracts because production data platforms fail when schema drift is unmanaged.
- I designed the project as a governed data product rather than a one-off notebook.
- I included privacy boundaries and responsible-use language because education data is sensitive.
- I produced executive artifacts so technical work connects to planning decisions.
