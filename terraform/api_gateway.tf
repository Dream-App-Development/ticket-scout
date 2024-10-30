# Define the API Gateway
resource "aws_api_gateway_rest_api" "api" {
  name        = "${var.app_ident}-api"
  description = "API Gateway for ${var.app_ident}"
}

# Define a resource within the API (e.g., a root endpoint)
resource "aws_api_gateway_resource" "resource" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "example"
}

# Define the method (GET, POST, etc.) on the API Gateway
resource "aws_api_gateway_method" "method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.resource.id
  http_method   = "ANY"
  authorization = "NONE"
  api_key_required = false
}

# Set up integration with Lambda
resource "aws_api_gateway_integration" "integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.resource.id
  http_method             = aws_api_gateway_method.method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda_function.invoke_arn
}

## Add necessary permissions for API Gateway to invoke Lambda
#resource "aws_lambda_permission" "api_gateway_permission" {
#  statement_id  = "AllowAPIGatewayInvoke"
#  action        = "lambda:InvokeFunction"
#  function_name = aws_lambda_function.lambda_function.function_name
#  principal     = "apigateway.amazonaws.com"
#  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
#}

# Deploy the API
resource "aws_api_gateway_deployment" "deployment" {
  depends_on  = [aws_api_gateway_integration.integration]
  rest_api_id = aws_api_gateway_rest_api.api.id
  stage_name  = "staging"
}
