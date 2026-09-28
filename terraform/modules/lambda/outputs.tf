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

output "lambda_security_group_id" {
  description = "Security group ID used by the Lambda function"
  value       = aws_security_group.lambda.id
}