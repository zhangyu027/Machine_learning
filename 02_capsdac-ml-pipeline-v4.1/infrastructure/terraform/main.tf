terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "capsdac_lake" {
  name                        = var.bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = false

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition { age = 90 }
    action { type = "SetStorageClass", storage_class = "NEARLINE" }
  }
}

resource "google_bigquery_dataset" "capsdac_analytics" {
  dataset_id  = var.dataset_id
  location    = "US"
  description = "CAPSDAC governed analytics, features, forecasts, and monitoring tables"
}

resource "google_bigquery_table" "statewide_forecast" {
  dataset_id = google_bigquery_dataset.capsdac_analytics.dataset_id
  table_id   = "statewide_forecast"
  deletion_protection = false
  schema = file("${path.module}/../bigquery/schemas/statewide_forecast_schema.json")
}

resource "google_bigquery_table" "vendor_forecast" {
  dataset_id = google_bigquery_dataset.capsdac_analytics.dataset_id
  table_id   = "vendor_forecast"
  deletion_protection = false
  schema = file("${path.module}/../bigquery/schemas/vendor_forecast_schema.json")
}

resource "google_artifact_registry_repository" "capsdac_containers" {
  location      = var.region
  repository_id = "capsdac-ml"
  description   = "CAPSDAC ML containers for API and training jobs"
  format        = "DOCKER"
}

resource "google_service_account" "runtime" {
  account_id   = var.service_account_id
  display_name = "CAPSDAC ML runtime service account"
}

locals {
  runtime_roles = [
    "roles/aiplatform.user",
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/storage.objectAdmin",
    "roles/artifactregistry.reader",
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter"
  ]
}

resource "google_project_iam_member" "runtime_roles" {
  for_each = toset(local.runtime_roles)
  project  = var.project_id
  role     = each.key
  member   = "serviceAccount:${google_service_account.runtime.email}"
}
