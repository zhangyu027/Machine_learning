provider "aws" { region = var.aws_region }

resource "aws_s3_bucket" "lake" { bucket = var.bucket_name }
resource "aws_kms_key" "healthcare" { description = "KMS key for healthcare multimodal platform" }
resource "aws_ecr_repository" "training" { name = "healthcare-mm-foundation-training" }
