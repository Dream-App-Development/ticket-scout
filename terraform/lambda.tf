variable "app_timeout" {
  description = "Number of seconds until the lambda function times out"
  type        = number
}

variable "app_memory" {
  description = "Number of megabytes of memory to allocate to the lambda function"
  type        = number
}

resource "aws_lambda_function" "lambda_function" {
  depends_on = [null_resource.push_image]
  function_name = var.app_ident
  role          = aws_iam_role.lambda_exec.arn
  package_type  = "Image"
  image_uri = "${aws_ecr_repository.ecr_repository.repository_url}:${null_resource.push_image.triggers.code_hash}"
  timeout = var.app_timeout
  memory_size = var.app_memory

  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }
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
