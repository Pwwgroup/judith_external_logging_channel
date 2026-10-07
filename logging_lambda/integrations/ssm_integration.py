"""Functions that enable integration with the AWS SSM service."""

import boto3
from botocore.exceptions import ClientError


def get_ssm_parameter(name: str, region: str) -> str:
    client = boto3.client("ssm", region_name=region)

    try:
        response = client.get_parameter(Name=name, WithDecryption=False)
        return response["Parameter"]["Value"]
    except client.exceptions.ParameterNotFound:
        raise
    except ClientError:
        raise
