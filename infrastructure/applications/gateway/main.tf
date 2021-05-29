locals {
  is_prod           = terraform.workspace == "production"
  domain            = local.is_prod ? "${local.domain_name}.python.it" : "${terraform.workspace}-${local.domain_name}.python.it"
  users_service_url = local.is_prod ? "https://users-api.python.it" : "https://${terraform.workspace}-users-api.python.it"
}

data "aws_iam_role" "lambda" {
  name = "pythonit-lambda-role"
}

module "lambda" {
  source = "../../components/application_lambda"

  application            = local.application
  docker_repository_name = "gateway"
  docker_tag             = terraform.workspace
  role_arn               = data.aws_iam_role.lambda.arn
  memory_size            = 1024

  env_vars = {
    NODE_ENV             = "production"
    VARIANT              = var.admin_variant ? "admin" : "default"
    SENTRY_DSN           = var.sentry_dsn
    APOLLO_KEY           = var.apollo_key
    APOLLO_GRAPH_ID      = var.admin_variant ? "admin-python-italia" : "default-python-italia"
    APOLLO_GRAPH_VARIANT = terraform.workspace
    USERS_SERVICE        = local.users_service_url
    # Secrets
    PASTAPORTO_SECRET         = var.pastaporto_secret
    IDENTITY_SECRET           = var.identity_secret
    SERVICE_TO_SERVICE_SECRET = var.service_to_service_secret
    PASTAPORTO_ACTION_SECRET  = var.pastaporto_action_secret
  }
}

module "api" {
  source = "../../components/http_api_gateway"

  application          = local.application
  lambda_invoke_arn    = module.lambda.invoke_arn
  lambda_function_name = module.lambda.function_name
}

data "aws_acm_certificate" "cert" {
  domain   = "*.python.it"
  statuses = ["ISSUED"]
  provider = aws.us
}

module "distribution" {
  source = "../../components/cloudfront"

  application     = local.application
  zone_name       = "python.it"
  domain          = local.domain
  certificate_arn = data.aws_acm_certificate.cert.arn
  origin_url      = module.api.cloudfront_friendly_endpoint
}
