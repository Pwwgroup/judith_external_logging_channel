"""CDK Stage to group all stacks for a given environment."""

from typing import Any

import aws_cdk as cdk

from judith_external_logging_channel.api_gateway_stack import ApiGatewayStack
from judith_external_logging_channel.config.config import EnvConfig
from judith_external_logging_channel.foundation_stack import FoundationStack
from judith_external_logging_channel.logging_lambda_stack import LoggingLambdaStack


class EnvironmentStage(cdk.Stage):
    """CDK Stage to group all stacks for a given environment."""

    def __init__(self, scope: cdk.App, stage_id: str, *, env_config: EnvConfig, **kwargs: Any) -> None:
        super().__init__(scope, stage_id, env=env_config.cdk_env(), **kwargs)

        self.foundation = FoundationStack(
            self,
            "FoundationStack",
            env_config=env_config,
        )

        self.api_gateway = ApiGatewayStack(
            self,
            "ApiGatewayStack",
            env_config=env_config,
        )

        self.logging_lambda_stack = LoggingLambdaStack(
            self,
            "JudithLoggingLambdaStack",
            env_config=env_config,
            vpc=self.foundation.vpc,
            api_gateway=self.api_gateway.api_gateway,
            authorizer=self.api_gateway.authorizer,
        )
    
        self.logging_lambda_stack.add_dependency(self.foundation)
        self.logging_lambda_stack.add_dependency(self.api_gateway)
