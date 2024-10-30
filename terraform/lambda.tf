variable "app_timeout" {
  description = "Number of seconds until the lambda function times out"
  type        = number
}

variable "app_memory" {
  description = "Number of megabytes of memory to allocate to the lambda function"
  type        = number
}

resource "aws_iam_role" "lambda_exec" {
  name = "${var.app_ident}_lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = "lambda.amazonaws.com",
        },
        Effect = "Allow",
      },
    ],
  })
}

resource "aws_iam_role_policy_attachment" "lambda_exec_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "lambda_function" {
  depends_on   = [null_resource.push_image]
  function_name = var.app_ident
  role          = aws_iam_role.lambda_exec.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.ecr_repository.repository_url}:${null_resource.push_image.triggers.code_hash}"
  timeout       = var.app_timeout
  memory_size   = var.app_memory

  environment {
    variables = {
      ENVIRONMENT = var.environment
      APP_IDENT = var.app_ident
    }
  }
}

# Define the API Gateway
resource "aws_api_gateway_rest_api" "api_gateway" {
  name = "${var.app_ident}-api"
  description = "API Gateway for ${var.app_ident}"
}

# Define the API Gateway resource path (for example, "/lambda")
resource "aws_api_gateway_resource" "lambda_resource" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  parent_id   = aws_api_gateway_rest_api.api_gateway.root_resource_id
  path_part   = "lambda"  # Adjust this to your desired path
}

# Define the API Gateway method
resource "aws_api_gateway_method" "get_lambda" {
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  resource_id   = aws_api_gateway_resource.lambda_resource.id
  http_method   = "POST"  # Change to "GET" or other HTTP method as needed
  authorization = "NONE"
}

# Define the Lambda integration for API Gateway
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api_gateway.id
  resource_id             = aws_api_gateway_resource.lambda_resource.id
  http_method             = aws_api_gateway_method.get_lambda.http_method
  integration_http_method = "POST"   # Must be POST for Lambda
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda_function.invoke_arn
}

# Grant API Gateway permission to invoke the Lambda function
resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api_gateway.execution_arn}/*/*"
}

# Output the API Gateway endpoint
output "api_gateway_endpoint" {
  value = "${aws_api_gateway_rest_api.api_gateway.execution_arn}/${aws_api_gateway_method.get_lambda.http_method}${aws_api_gateway_resource.lambda_resource.path_part}"
}
