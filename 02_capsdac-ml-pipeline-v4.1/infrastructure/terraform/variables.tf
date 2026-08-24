variable "project_id" {
  description = "GCP project id, for example capsdac2-ml"
  type        = string
}

variable "region" {
  description = "Primary GCP region"
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
  description = "Globally unique GCS bucket for CAPSDAC lake/model artifacts"
  type        = string
}

variable "dataset_id" {
  description = "BigQuery dataset for CAPSDAC analytics"
  type        = string
  default     = "capsdac_analytics"
}

variable "service_account_id" {
  description = "Service account for Vertex AI / Cloud Run workloads"
  type        = string
  default     = "capsdac-ml-runtime"
}
