output "lambda_function_name" {
  description = "Name of the CRM Lambda function"
  value       = aws_lambda_function.crm_api.function_name
}

output "lambda_function_arn" {
  description = "ARN of the CRM Lambda function"
  value       = aws_lambda_function.crm_api.arn
}

output "lambda_role_arn" {
  description = "ARN of the Lambda execution role"
  value       = aws_iam_role.lambda_execution.arn
}