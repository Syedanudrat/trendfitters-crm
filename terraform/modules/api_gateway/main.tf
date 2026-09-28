resource "aws_apigatewayv2_api" "crm_api" {
  name          = "${var.project_name}-${var.environment}-api"
  protocol_type = "HTTP"

  tags = var.tags
}

resource "aws_apigatewayv2_integration" "crm_lambda" {
  api_id = aws_apigatewayv2_api.crm_api.id

  integration_type   = "AWS_PROXY"
  integration_uri    = var.lambda_arn
  integration_method = "POST"

  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "health" {
  api_id = aws_apigatewayv2_api.crm_api.id

  route_key = "GET /health"
  target    = "integrations/${aws_apigatewayv2_integration.crm_lambda.id}"
}

resource "aws_apigatewayv2_route" "customers" {
  api_id    = aws_apigatewayv2_api.crm_api.id

  route_key = "POST /customers"
  target    = "integrations/${aws_apigatewayv2_integration.crm_lambda.id}"
}

resource "aws_apigatewayv2_route" "customers_get" {
  api_id = aws_apigatewayv2_api.crm_api.id

  route_key = "GET /customers"
  target    = "integrations/${aws_apigatewayv2_integration.crm_lambda.id}"
}

resource "aws_apigatewayv2_route" "customer_by_id" {
  api_id = aws_apigatewayv2_api.crm_api.id

  route_key = "GET /customers/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.crm_lambda.id}"
}

resource "aws_apigatewayv2_route" "customer_delete" {
  api_id = aws_apigatewayv2_api.crm_api.id

  route_key = "DELETE /customers/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.crm_lambda.id}"
}

resource "aws_apigatewayv2_route" "customer_update" {
  api_id = aws_apigatewayv2_api.crm_api.id

  route_key = "PUT /customers/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.crm_lambda.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.crm_api.id

  name        = "$default"
  auto_deploy = true

  tags = var.tags
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id = "AllowAPIGatewayInvoke"

  action = "lambda:InvokeFunction"

  function_name = var.lambda_function_name

  principal = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.crm_api.execution_arn}/*/*"
}

resource "aws_apigatewayv2_route" "leads" {
  api_id = aws_apigatewayv2_api.crm_api.id

  route_key = "POST /leads"
  target    = "integrations/${aws_apigatewayv2_integration.crm_lambda.id}"
}

resource "aws_apigatewayv2_route" "opportunities" {
  api_id = aws_apigatewayv2_api.crm_api.id

  route_key = "POST /opportunities"
  target    = "integrations/${aws_apigatewayv2_integration.crm_lambda.id}"
}

resource "aws_apigatewayv2_route" "opportunities_get" {
  api_id = aws_apigatewayv2_api.crm_api.id

  route_key = "GET /opportunities"
  target    = "integrations/${aws_apigatewayv2_integration.crm_lambda.id}"
}

resource "aws_apigatewayv2_route" "orders" {
  api_id = aws_apigatewayv2_api.crm_api.id

  route_key = "POST /orders"
  target    = "integrations/${aws_apigatewayv2_integration.crm_lambda.id}"
}

resource "aws_apigatewayv2_route" "orders_get" {
  api_id = aws_apigatewayv2_api.crm_api.id

  route_key = "GET /orders"
  target    = "integrations/${aws_apigatewayv2_integration.crm_lambda.id}"
}

resource "aws_apigatewayv2_route" "leads_get" {
  api_id = aws_apigatewayv2_api.crm_api.id

  route_key = "GET /leads"
  target    = "integrations/${aws_apigatewayv2_integration.crm_lambda.id}"
}