output "db_instance_endpoint" {
  description = "RDS database endpoint"
  value       = aws_db_instance.crm.address
}

output "db_instance_port" {
  description = "RDS database port"
  value       = aws_db_instance.crm.port
}

output "db_instance_id" {
  description = "RDS database identifier"
  value       = aws_db_instance.crm.identifier
}