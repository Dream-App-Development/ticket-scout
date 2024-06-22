#
# terraform {
#   required_providers {
#     aws = {
#       source  = "hashicorp/aws"
#       version = "~> 4.0"
#     }
#   }
# }
#
# provider "aws" {
#   region = "ap-southeast-1"
# }
#
# provider "aws" {
#   alias  = "apsoutheast1"
#   region = "ap-southeast-1"
# }
#
# data "aws_region" "current" {}
# data "aws_caller_identity" "current" {}
# data "aws_vpc" "selected" {
#   default = true
# }
# data "aws_subnets" "subnets" {
#   filter {
#     name   = "vpc-id"
#     values = [data.aws_vpc.selected.id]
#   }
# }
#
# variable "app_ident" {
#   description = "Identifier of the application"
#   type = string
# }
#
# variable "environment" {
#   type = string
# }

