#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Stage, App
from typing import Any

from judith_external_logging_channel.config.config import EnvConfig
from judith_external_logging_channel.environment_stage import EnvironmentStage


app = cdk.App()

context_env = app.node.try_get_context("env") or "dev"
account = app.node.try_get_context("accountId") or os.getenv("CDK_DEFAULT_ACCOUNT")
region = app.node.try_get_context("region") or os.getenv("CDK_DEFAULT_REGION")

if not account or not region or not context_env:
    raise ValueError(
        "Account, region, and environment must be specified either in context or as environment variables"
    )

cfg_dev = EnvConfig(env_id=context_env, account=account, region=region)

EnvironmentStage(app, "JudithLoggingDev", env_config=cfg_dev)

app.synth()
