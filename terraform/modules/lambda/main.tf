data "archive_file" "crm_lambda" {
  type        = "zip"
  source_file = "${path.root}/../../../application/lambda/crm-api/lambda_function.py"
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

resource "aws_lambda_function" "crm_api" {
  function_name = "${var.project_name}-${var.environment}-crm-api"

  filename         = data.archive_file.crm_lambda.output_path
  source_code_hash = data.archive_file.crm_lambda.output_base64sha256

  role = aws_iam_role.lambda_execution.arn

  handler = "lambda_function.lambda_handler"
  runtime = "python3.13"

  timeout     = 10
  memory_size = 256

  tags = var.tags
}