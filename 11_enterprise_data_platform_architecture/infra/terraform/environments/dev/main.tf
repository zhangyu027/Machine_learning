module "platform" {
  source      = "../../modules/platform"
  name_prefix = "edp"
  environment = "dev"
  location    = "westus2"
  tags = {
    owner       = "enterprise-data-platform"
    environment = "dev"
    managed_by  = "terraform"
  }
}
