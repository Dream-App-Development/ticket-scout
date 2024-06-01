data "aws_ecr_repository" "existing" {
  name = "${var.app_ident}_repository"
}

resource "aws_ecr_repository" "ecr_repository" {
  count = length(data.aws_ecr_repository.existing.id) == 0 ? 1 : 0
  name = "${var.app_ident}_repository"
}

variable "code_hash_file" {
  description = "Filename of the code hash file"
  type        = string
}

resource "null_resource" "push_image" {
  triggers = {
    code_hash = filemd5(var.code_hash_file)
    ecr_repo = aws_ecr_repository.ecr_repository.repository_url
    force = 4
  }

  provisioner "local-exec" {
    command = <<EOF
    set -e # Exit immediately if a command exits with a non-zero status.
    cd ..

    echo "Running docker build: ${path.cwd}"

    echo "Log into AWS ECR Container Repository"
    aws ecr get-login-password \
      --region ${data.aws_region.current.name} | \
      docker login \
        --username AWS \
        --password-stdin ${aws_ecr_repository.ecr_repository.repository_url}

    echo "Build the Docker Image"

    # docker build \
    # docker buildx build --platform linux/amd64 \
    docker build \
      -t ${aws_ecr_repository.ecr_repository.repository_url}:${self.triggers.code_hash} \
      -t ${aws_ecr_repository.ecr_repository.repository_url}:latest \
      .

    echo "Push Docker Image to AWS ECR Container Repository"
    docker push ${aws_ecr_repository.ecr_repository.repository_url}:${self.triggers.code_hash}
    docker push ${aws_ecr_repository.ecr_repository.repository_url}:latest
    sleep 10
    EOF
  }
}
