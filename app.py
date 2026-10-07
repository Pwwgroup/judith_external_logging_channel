#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Stage, App
from typing import Any

from logging_lambda.api_gateway_stack import ExternalLoggerGatewayStack
from logging_lambda.logging_lambda_stack import LoggingLambdaStack
from logging_lambda.config.config import EnvConfig


class EnvironmentStage(Stage):
    def __init__(
        self, scope: App, stage_id: str, *, env_config: EnvConfig, **kwargs: Any
    ) -> None:
        super().__init__(scope, stage_id, env=env_config.cdk_env(), **kwargs)

        self.logging_lambda_stack = LoggingLambdaStack(
            self, "LoggingLambdaStack", env_config=env_config
        )

        self.api_gateway_stack = ExternalLoggerGatewayStack(
            self,
            "ExternalLoggerApiGatewayStack",
            env_config=env_config,
            logging_lambda=self.logging_lambda_stack.external_logging_lambda,
        )
        self.api_gateway_stack.add_dependency(self.logging_lambda_stack)


app = cdk.App()

context_env = app.node.try_get_context("env") or "dev"
account = app.node.try_get_context("accountId") or os.getenv("CDK_DEFAULT_ACCOUNT")
region = app.node.try_get_context("region") or os.getenv("CDK_DEFAULT_REGION")

if not account or not region or not context_env:
    raise ValueError(
        "Account, region, and environment must be specified either in context or as environment variables"
    )

cfg_dev = EnvConfig(env_id=context_env, account=account, region=region)

EnvironmentStage(app, "LoggingLambdaStage", env_config=cfg_dev)

app.synth()
