from aws_cdk import Duration, aws_lambda, aws_apigateway
from logging_lambda.integrations.ssm_integration import get_ssm_parameter
from logging_lambda.base_stack import BaseStack
from logging_lambda.config.config import EnvConfig

from typing import Any
from constructs import Construct


class ExternalLoggerGatewayStack(BaseStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        env_config: EnvConfig,
        logging_lambda: aws_lambda.Function,
        route_segment: str = "external_logger",
        authorizer_header: str = "Authorization",
        **kwargs: Any,
    ) -> None:
        super().__init__(scope, id, env_config=env_config, **kwargs)

        api_id_param = f"/prometheus/harriet/{env_config.env_id}/api-gateway-id"
        api_root_param = (
            f"/prometheus/harriet/{env_config.env_id}/api-gateway-root-resource-id"
        )
        authorizer_arn_param = (
            f"/prometheus/harriet/{env_config.env_id}/api-lambda-authorizer-arn"
        )

        api_gateway_id = get_ssm_parameter(name=api_id_param, region=env_config.region)
        api_gateway_root_resource_id = get_ssm_parameter(
            name=api_root_param, region=env_config.region
        )
        authorizer_arn = get_ssm_parameter(
            name=authorizer_arn_param, region=env_config.region
        )

        api = aws_apigateway.RestApi.from_rest_api_attributes(
            self,
            self.name("ExternalLoggerApiGateway"),
            rest_api_id=api_gateway_id,
            root_resource_id=api_gateway_root_resource_id,
        )

        authorizer_func = aws_lambda.Function.from_function_arn(
            self,
            self.name("AuthorizerFunction"),
            function_arn=authorizer_arn,
        )

        authorizer = aws_apigateway.RequestAuthorizer(
            self,
            self.name("ExternalLoggerRequestAuthorizer"),
            handler=authorizer_func,
            identity_sources=[f"method.request.header.{authorizer_header}"],
            results_cache_ttl=Duration.seconds(0),
        )

        route_resource = api.root.add_resource(route_segment)

        log_resource = route_resource.add_resource("extrernal_log")

        log_resource.add_method(
            "POST",
            aws_apigateway.LambdaIntegration(logging_lambda),
            authorization_type=aws_apigateway.AuthorizationType.CUSTOM,
            authorizer=authorizer,
        )
