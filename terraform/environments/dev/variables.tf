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

variable "vpc_cidr" {
  description = "CIDR block for the DEV VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
  description = "CIDR block for the private subnet"
  type        = string
  default     = "10.0.2.0/24"
}

variable "availability_zone" {
  description = "Availability Zone for DEV"
  type        = string
  default     = "ap-south-1a"
}

variable "rds_instance_class" {
  description = "RDS instance class for DEV"
  type        = string
  default     = "db.t4g.micro"
}

variable "rds_allocated_storage" {
  description = "Initial RDS storage in GB"
  type        = number
  default     = 20
}

variable "rds_max_allocated_storage" {
  description = "Maximum RDS storage in GB"
  type        = number
  default     = 100
}

variable "database_name" {
  description = "CRM database name"
  type        = string
  default     = "trendfitters"
}

variable "database_username" {
  description = "CRM database username"
  type        = string
  default     = "crmadmin"
}

variable "database_password" {
  description = "CRM database password"
  type        = string
  sensitive   = true
}

variable "private_subnet_2_cidr" {
  description = "CIDR block for the second private subnet"
  type        = string
  default     = "10.0.3.0/24"
}

variable "availability_zone_2" {
  description = "Second Availability Zone for DEV"
  type        = string
  default     = "ap-south-1b"
}