"""Base stack class for the logging Lambda CDK app."""

from typing import Any

from aws_cdk import RemovalPolicy, Stack, Tags
from constructs import Construct

from logging_lambda.config.config import EnvConfig


class BaseStack(Stack):
    def __init__(
        self, scope: Construct, id: str, *, env_config: EnvConfig, **kwargs: Any
    ) -> None:
        super().__init__(scope, id, env=env_config.cdk_env(), **kwargs)
        self.env_config = env_config
        Tags.of(self).add("App", "LoggingLambda")
        Tags.of(self).add("Env", self.env_config.env_id)

    @property
    def removal(self) -> RemovalPolicy:
        return (
            RemovalPolicy.RETAIN if self.env_config.is_prod else RemovalPolicy.DESTROY
        )

    def name(self, suffix: str) -> str:
        return f"LoggingLambda-{self.env_config.env_id}-{suffix}"
