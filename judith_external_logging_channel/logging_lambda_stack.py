from aws_cdk import Duration
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_logs as logs
from aws_cdk import aws_ec2 as ec2

from judith_external_logging_channel.foundation_stack import FoundationStack
from judith_external_logging_channel.config.config import EnvConfig

from constructs import Construct


class LoggingLambdaStack(FoundationStack):
    def __init__(
        self, scope: Construct, id: str, env_config: EnvConfig, vpc: ec2.IVpc, api_gateway: apigateway.IRestApi, authorizer: apigateway.IAuthorizer, **kwargs
    ) -> None:
        super().__init__(scope, id, env_config=env_config, **kwargs)

        self.external_logging_lambda = self._create_lambda_function()
        self.vpc = vpc
        self.api_gateway = api_gateway
        self.authorizer = authorizer
        self._configure_route()

    def _create_lambda_function(self):
        fn = _lambda.Function(
            self,
            self.name("LoggingLambda"),
            description="Writes logs from external process to internal AWS cloudwatch store",
            vpc=self.vpc,
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="app.handler",
            code=_lambda.Code.from_asset("src/logging_lambda"),
            environment={
                "ENVIRONMENT": self.env_config.env_id,
                "ENV_AWS_REGION": self.env_config.region,
            },
            timeout=Duration.seconds(20),
            memory_size=128,
            log_retention=logs.RetentionDays.ONE_MONTH,
        )
        return fn
    
    def _configure_route(self) -> None:
        route_resource = self.api_gateway.root.add_resource("external_logger")
        log_resource = route_resource.add_resource("insert")
        
        log_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(self.external_logging_lambda),
            authorization_type=apigateway.AuthorizationType.CUSTOM,
            authorizer=self.authorizer,
        )
        log_resource.add_cors_preflight(
            allow_origins=["*"],
            allow_methods=["POST", "OPTIONS"],
            allow_headers=["Content-Type", "Authorization", "X-Amz-Date", "X-Api-Key", "X-Amz-Security-Token"],
        )

