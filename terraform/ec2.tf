resource "aws_instance" "example" {
  ami = "ami-0c55b159cbfafe1f0"  # Update with the appropriate AMI ID for your region
  instance_type = "t2.micro"
  subnet_id     = data.aws_subnets.subnets.ids[0]

  tags = {
    Name = "${var.app_ident}-${var.environment}-instance"
  }
}

output "instance_id" {
  value = aws_instance.example.id
}