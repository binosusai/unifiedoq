terraform {
  required_version = ">= 1.6.0"
}

# Shared-platform infrastructure entrypoint for: Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys
# Keep this file small. Prefer shared modules from:
# /home/runner/work/ideate/platform/terraform-modules

variable "project_name" {
  type    = string
  default = "unifiedoq"
}

variable "use_shared_platform" {
  type    = bool
  default = true
}

module "frontend" {
  source       = "/home/runner/work/ideate/platform/terraform-modules/vercel-static-site"
  project_name = var.project_name
}

module "api" {
  source       = "/home/runner/work/ideate/platform/terraform-modules/aws-python-api"
  project_name = var.project_name
}

# Enable when this POC needs hosted Postgres.
# module "database" {
#   source       = "/home/runner/work/ideate/platform/terraform-modules/neon-postgres"
#   project_name = var.project_name
# }
