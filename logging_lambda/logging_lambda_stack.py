from aws_cdk import Duration
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as logs

from logging_lambda.base_stack import BaseStack
from logging_lambda.config.config import EnvConfig

from constructs import Construct


class LoggingLambdaStack(BaseStack):
    def __init__(
        self, scope: Construct, id: str, env_config: EnvConfig, **kwargs
    ) -> None:
        super().__init__(scope, id, env_config=env_config, **kwargs)

        self.external_logging_lambda = self._create_lambda_function()

    def _create_lambda_function(self):
        fn = _lambda.Function(
            self,
            self.name("LoggingLambda"),
            description="Writes logs from external process to internal AWS cloudwatch store",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="app.handler",
            code=_lambda.Code.from_asset("src/logging_lambda"),
            environment={
                "ENVIRONMENT": self.env_config.env_id,
                "ENV_AWS_REGION": self.env_config.region,
            },
            timeout=Duration.seconds(60),
            memory_size=128,
            log_retention=logs.RetentionDays.ONE_MONTH,
        )
        return fn
