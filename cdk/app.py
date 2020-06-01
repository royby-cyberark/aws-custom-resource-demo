#!/usr/bin/env python3

from aws_cdk import core

from cdk.cdk_stack import CdkStack


app = core.App()
CdkStack(scope=app, id="AwsS3ObjectCustomResourceDemo")

app.synth()
