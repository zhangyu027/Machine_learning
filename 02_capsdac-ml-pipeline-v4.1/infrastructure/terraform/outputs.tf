output "bucket_name" { value = google_storage_bucket.capsdac_lake.name }
output "dataset_id" { value = google_bigquery_dataset.capsdac_analytics.dataset_id }
output "artifact_repository" { value = google_artifact_registry_repository.capsdac_containers.repository_id }
output "runtime_service_account" { value = google_service_account.runtime.email }
