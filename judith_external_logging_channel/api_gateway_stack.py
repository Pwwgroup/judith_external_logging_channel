from aws_cdk import Duration, aws_lambda, aws_apigateway

from typing import Any
from constructs import Construct


from typing import Any

from aws_cdk import aws_apigateway as apigateway
from constructs import Construct




from judith_external_logging_channel.foundation_stack import FoundationStack
from judith_external_logging_channel.integrations.ssm_integration import get_ssm_parameter
from judith_external_logging_channel.config.config import EnvConfig

from judith_external_logging_channel.imported_authorizer import ImportedAuthorizer


class ApiGatewayReference:
    """Helper class to extract SSM parameters for the shared API Gateway."""

    def __init__(self, env_config: EnvConfig) -> None:
        prefix = f"/prometheus/harriet/{env_config.env_id}"

        self.api_gateway_id = get_ssm_parameter(f"{prefix}/api-gateway-id", region=env_config.region)
        self.root_resource_id = get_ssm_parameter(f"{prefix}/api-gateway-root-resource-id", region=env_config.region)
        self.authorizer_id = get_ssm_parameter(f"{prefix}/api-gateway-authorizer-id", region=env_config.region)


class ApiGatewayStack(FoundationStack):
    def __init__(self, scope: Construct, id: str, *, env_config: EnvConfig, **kwargs: Any) -> None:
        super().__init__(scope, id, env_config=env_config, **kwargs)
        self.api_gateway_references = ApiGatewayReference(env_config=env_config)
        self.authorizer: apigateway.IAuthorizer = ImportedAuthorizer(self.api_gateway_references.authorizer_id)
        
        self.api_gateway = apigateway.RestApi.from_rest_api_attributes(
            self,
            self.name("SharedApiGateway"),
            rest_api_id=self.api_gateway_references.api_gateway_id,
            root_resource_id=self.api_gateway_references.root_resource_id,
        )



# class ExternalLoggerGatewayStack(BaseStack):
#     def __init__(
#         self,
#         scope: Construct,
#         id: str,
#         *,
#         env_config: EnvConfig,
#         logging_lambda: aws_lambda.Function,
#         route_segment: str = "external_logger",
#         authorizer_header: str = "Authorization",
#         **kwargs: Any,
#     ) -> None:
#         super().__init__(scope, id, env_config=env_config, **kwargs)

#         route_resource = api.root.add_resource(route_segment)

#         log_resource = route_resource.add_resource("external_log")

#         log_resource.add_method(
#             "POST",
#             aws_apigateway.LambdaIntegration(logging_lambda),
#             authorization_type=aws_apigateway.AuthorizationType.CUSTOM,
#             authorizer=authorizer,
#         )
