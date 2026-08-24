# AWS Productionization Design

## Target AWS services

- **Amazon S3**: raw/bronze/silver/gold lakehouse storage.
- **AWS Glue**: PySpark transformations, schema normalization, and Data Catalog registration.
- **AWS Step Functions**: orchestration with retries and failure handling.
- **Amazon SageMaker**: model training, model registry, batch forecast jobs, and monitoring.
- **Amazon Athena**: SQL access for analysts and reporting tools.
- **Amazon QuickSight**: executive dashboards.
- **CloudWatch**: job metrics, data quality alarms, and pipeline observability.
- **KMS/IAM/Lake Formation**: encryption, access control, and governance.

## Production workflow

1. Land monthly source extracts in S3 bronze.
2. Run Glue validation and conformance jobs into silver parquet.
3. Build site/vendor/statewide gold feature tables.
4. Train or refresh the forecast model in SageMaker.
5. Run recursive batch forecasts and write output to gold.
6. Publish Athena tables and dashboard-ready artifacts.
7. Monitor row counts, schema changes, missing vendors/sites, and forecast drift.
