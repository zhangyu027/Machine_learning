terraform {
  required_version = ">= 1.7.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

variable "name_prefix" { type = string }
variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "environment must be dev, test, or prod"
  }
}
variable "location" { type = string }
variable "tags" { type = map(string) }

# Reference-only module boundary. Add approved Azure resources through reviewed modules.
output "resource_naming_prefix" {
  value = "${var.name_prefix}-${var.environment}"
}
