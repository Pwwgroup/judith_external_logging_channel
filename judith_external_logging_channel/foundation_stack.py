"""Foundation stack -- imports the shared VPC from SSM."""

from typing import Any

from aws_cdk import CfnOutput
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

from judith_external_logging_channel.base_stack import BaseStack
from judith_external_logging_channel.config.config import EnvConfig
from judith_external_logging_channel.integrations.ssm_integration import get_ssm_parameter


class FoundationStack(BaseStack):
    """Looks up the shared Prometheus VPC and exposes it as ``self.vpc``.

    Split out from the pipeline stack so any future Hazel Lambda/service can
    take a dependency on the VPC (via ``vpc=foundation.vpc``) without needing
    to redo the SSM lookup or restructure an existing stack.
    """

    def __init__(self, scope: Construct, id: str, *, env_config: EnvConfig, **kwargs: Any) -> None:
        super().__init__(scope, id, env_config=env_config, **kwargs)

        vpc_param = f"/prometheus/gertrude/{env_config.env_id}/vpcid"
        vpc_id = get_ssm_parameter(name=vpc_param, region=env_config.region)

        self.vpc = ec2.Vpc.from_lookup(self, "Vpc", vpc_id=vpc_id)
        CfnOutput(self, "VpcId", value=self.vpc.vpc_id)
