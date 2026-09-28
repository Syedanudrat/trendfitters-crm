variable "aws_region" {
  description = "AWS region for the DEV environment"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "trendfitters-crm"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "tags" {
  description = "Common resource tags"
  type        = map(string)

  default = {
    Project   = "TrendFitters-CRM"
    ManagedBy = "Terraform"
  }
}