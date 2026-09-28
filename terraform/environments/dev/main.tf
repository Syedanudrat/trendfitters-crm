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

  vpc_id = module.vpc.vpc_id

  private_subnet_ids = [
    module.vpc.private_subnet_id,
    module.vpc.private_subnet_2_id
  ]

  vpc_cidr = var.vpc_cidr

  database_host     = module.rds.db_instance_endpoint
  database_port     = module.rds.db_instance_port
  database_name     = var.database_name
  database_username = var.database_username
  database_password = var.database_password

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

module "vpc" {
  source = "../../modules/vpc"

  project_name = var.project_name
  environment  = var.environment

  vpc_cidr            = var.vpc_cidr
  public_subnet_cidr  = var.public_subnet_cidr
  private_subnet_cidr = var.private_subnet_cidr
  availability_zone   = var.availability_zone

  private_subnet_2_cidr = var.private_subnet_2_cidr
  availability_zone_2   = var.availability_zone_2

  tags = var.tags
}

module "rds" {
  source = "../../modules/rds"

  project_name = var.project_name
  environment  = var.environment

  instance_class        = var.rds_instance_class
  allocated_storage     = var.rds_allocated_storage
  max_allocated_storage = var.rds_max_allocated_storage

  database_name     = var.database_name
  database_username = var.database_username
  database_password = var.database_password

  private_subnet_ids = [
    module.vpc.private_subnet_id,
    module.vpc.private_subnet_2_id
  ]

  vpc_id                   = module.vpc.vpc_id
  allowed_cidr             = var.vpc_cidr
  lambda_security_group_id = module.crm_lambda.lambda_security_group_id

  tags = var.tags
}