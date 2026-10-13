from typing import Any
from constructs import Construct

from aws_cdk import aws_apigateway as apigateway

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
