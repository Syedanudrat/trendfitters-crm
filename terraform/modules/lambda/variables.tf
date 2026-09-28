variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
}

variable "tags" {
  description = "Tags applied to AWS resources"
  type        = map(string)
  default     = {}
}                   

variable "vpc_id" {
  description = "VPC ID for Lambda"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for Lambda"
  type        = list(string)
}

variable "database_host" {
  description = "RDS database hostname"
  type        = string
}

variable "database_port" {
  description = "RDS database port"
  type        = number
  default     = 5432
}

variable "database_name" {
  description = "CRM database name"
  type        = string
}

variable "database_username" {
  description = "CRM database username"
  type        = string
}

variable "database_password" {
  description = "CRM database password"
  type        = string
  sensitive   = true
}

variable "vpc_cidr" {
  description = "VPC CIDR allowed for Lambda outbound database traffic"
  type        = string
}