terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = "trendfitters"
}

module "crm_lambda" {
  source = "../../modules/lambda"

  project_name = var.project_name
  environment  = var.environment

  tags = var.tags
}

module "api_gateway" {
  source = "../../modules/api_gateway"

  project_name = var.project_name
  environment  = var.environment

  lambda_arn           = module.crm_lambda.lambda_function_arn
  lambda_function_name = module.crm_lambda.lambda_function_name

  tags = var.tags
}