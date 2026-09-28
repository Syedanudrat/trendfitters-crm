output "crm_lambda_function_name" {
  description = "CRM Lambda function name"
  value       = module.crm_lambda.lambda_function_name
}

output "crm_lambda_function_arn" {
  description = "CRM Lambda function ARN"
  value       = module.crm_lambda.lambda_function_arn
}

output "crm_api_endpoint" {
  description = "CRM API Gateway endpoint"
  value       = module.api_gateway.api_endpoint
}

output "crm_db_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = module.rds.db_instance_endpoint
}

output "crm_db_port" {
  description = "RDS PostgreSQL port"
  value       = module.rds.db_instance_port
}

output "frontend_bucket_name" {
  description = "S3 bucket used for the Trend Fitters CRM frontend"
  value       = module.frontend.frontend_bucket_name
}

output "frontend_website_endpoint" {
  description = "Trend Fitters CRM frontend website endpoint"
  value       = module.frontend.frontend_website_endpoint
}