locals {
  is_prod = terraform.workspace == "production"
  domain  = local.is_prod ? "${local.domain_name}.beta.python.it" : "${terraform.workspace}-${local.domain_name}.beta.python.it"

  # TODO: Need to coordinate between env and vercel
  association_frontend_url = "https://associazione.python.it"
}

data "aws_db_instance" "database" {
  db_instance_identifier = "pythonit-${terraform.workspace}"
}

data "aws_iam_role" "lambda" {
  name = "pythonit-lambda-role"
}

data "aws_vpc" "default" {
  filter {
    name   = "tag:Name"
    values = ["pythonit-vpc"]
  }
}

data "aws_subnet_ids" "private" {
  vpc_id = data.aws_vpc.default.id

  tags = {
    Type = "private"
  }
}

data "aws_security_group" "rds" {
  name = "pythonit-rds-security-group"
}

module "lambda" {
  source = "../../components/application_lambda"

  application        = local.application
  docker_tag         = terraform.workspace
  role_arn           = data.aws_iam_role.lambda.arn
  subnet_ids         = [for subnet in data.aws_subnet_ids.private.ids : subnet]
  security_group_ids = [data.aws_security_group.rds.id]
  env_vars = {
    DEBUG                     = "false"
    SECRET_KEY                = var.secret_key
    GOOGLE_AUTH_CLIENT_ID     = var.google_auth_client_id
    GOOGLE_AUTH_CLIENT_SECRET = var.google_auth_client_secret
    DATABASE_URL              = "postgresql+asyncpg://${data.aws_db_instance.database.master_username}:${var.database_password}@${data.aws_db_instance.database.address}:${data.aws_db_instance.database.port}/users"
    EMAIL_BACKEND             = "pythonit_toolkit.emails.backends.ses.SESEmailBackend"

    # Services
    ASSOCIATION_FRONTEND_URL = local.association_frontend_url

    # Secrets
    PASTAPORTO_SECRET         = var.pastaporto_secret
    IDENTITY_SECRET           = var.identity_secret
    SERVICE_TO_SERVICE_SECRET = var.service_to_service_secret
    PASTAPORTO_ACTION_SECRET  = var.pastaporto_action_secret
  }
}

data "aws_acm_certificate" "beta" {
  domain   = "*.beta.python.it"
  statuses = ["ISSUED"]
}

module "api" {
  source = "../../components/http_api_gateway"

  application          = local.application
  use_domain           = true
  domain               = local.domain
  zone_name            = "python.it"
  certificate_arn      = data.aws_acm_certificate.beta.arn
  lambda_invoke_arn    = module.lambda.invoke_arn
  lambda_function_name = module.lambda.function_name
}