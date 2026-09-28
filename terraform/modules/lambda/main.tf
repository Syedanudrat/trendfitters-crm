resource "aws_security_group" "lambda" {
  name        = "${var.project_name}-${var.environment}-lambda-sg"
  description = "Security group for TrendFitters CRM Lambda"
  vpc_id      = var.vpc_id

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-lambda-sg"
  })
}

resource "aws_vpc_security_group_egress_rule" "lambda_to_vpc" {
  security_group_id = aws_security_group.lambda.id

  ip_protocol = "tcp"
  from_port   = 5432
  to_port     = 5432
  cidr_ipv4   = var.vpc_cidr
}

data "archive_file" "crm_lambda" {
  type        = "zip"
  source_dir  = "${path.root}/../../../application/lambda/crm-api"
  output_path = "${path.root}/crm-api.zip"
}

resource "aws_iam_role" "lambda_execution" {
  name = "${var.project_name}-${var.environment}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "lambda.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_lambda_function" "crm_api" {
  function_name = "${var.project_name}-${var.environment}-crm-api"

  filename         = data.archive_file.crm_lambda.output_path
  source_code_hash = data.archive_file.crm_lambda.output_base64sha256

  role = aws_iam_role.lambda_execution.arn

  handler = "lambda_function.lambda_handler"
  runtime = "python3.13"

  vpc_config {
  subnet_ids         = var.private_subnet_ids
  security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
  variables = {
    DB_HOST     = var.database_host
    DB_PORT     = tostring(var.database_port)
    DB_NAME     = var.database_name
    DB_USER     = var.database_username
    DB_PASSWORD = var.database_password
  }
 }

  timeout     = 10
  memory_size = 256

  tags = var.tags
}