variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t4g.micro"
}

variable "allocated_storage" {
  description = "Initial storage in GB"
  type        = number
  default     = 20
}

variable "max_allocated_storage" {
  description = "Maximum storage in GB"
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
}

variable "database_password" {
  description = "CRM database password"
  type        = string
  sensitive   = true
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for RDS"
  type        = list(string)
}

variable "tags" {
  description = "Common resource tags"
  type        = map(string)
  default     = {}
}

variable "vpc_id" {
  description = "VPC ID where RDS security group will be created"
  type        = string
}

variable "allowed_cidr" {
  description = "CIDR allowed to connect to PostgreSQL"
  type        = string
}

variable "lambda_security_group_id" {
  description = "Security group ID of the Lambda function"
  type        = string
}