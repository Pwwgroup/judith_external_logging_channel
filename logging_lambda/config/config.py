"""Config classes for deployment statuses"""

from dataclasses import dataclass

import aws_cdk as cdk


@dataclass(frozen=True)
class EnvConfig:
    """Configuration for different deployment environments."""

    env_id: str
    account: str
    region: str = "eu-west-2"

    @property
    def is_prod(self) -> bool:
        """Check if the environment is production."""
        return self.env_id.lower() == "prod"

    def cdk_env(self) -> cdk.Environment:
        """Get the AWS CDK environment configuration."""
        return cdk.Environment(account=self.account, region=self.region)
