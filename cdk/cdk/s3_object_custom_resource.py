from typing import Any
from aws_cdk import (
    core,
    aws_iam as iam,
    aws_s3 as s3,
)

from aws_cdk.custom_resources import (
    AwsCustomResource,
    AwsCustomResourcePolicy,
    AwsSdkCall,
    PhysicalResourceId,
)


class S3ObjectResource(core.Construct):
    """S3 Object constructs that uses AWSCustomResource internally
    Arguments:
        :param bucket_name -- The Bucket name to create the s3 object in
        :param object_key -- Object key to create, to create in a folder, pass the full path including a folder, e.g: myfolder/myobject
        :param object_content - object content
        :param log_retention: The number of days log events of the Lambda function implementing this custom resource are kept in CloudWatch Logs. 
                              Default: logs.RetentionDays.INFINITE
    """

    def __init__(self, scope: core.Construct, id: str, bucket_name: str, object_key: str, object_content: Any, log_retention=None) -> None:
        super().__init__(scope, id)
        # The code that defines your stack goes here

        # This code is for demo puposes, we could have simple passed the bucket arn, but you can use this with bucket external to your stack
        target_bucket = s3.Bucket.from_bucket_name(
            scope=scope, id="CustomResourceDemoBucketExternal", bucket_name=bucket_name)

        on_create = self.get_on_create_update(
            bucket_name=bucket_name, object_key=object_key, object_content=object_content)
        on_update = on_create  # Updating an S3 object is actually creating a new version
        on_delete = self.get_on_delete(bucket_name, object_key)

        policy = AwsCustomResourcePolicy.from_sdk_calls(
            resources=[f'{target_bucket.bucket_arn}/{object_key}'])
        lambda_role = self.get_provisioning_lambda_role(construct_id=id)

        AwsCustomResource(scope=scope,
                          id=f'{id}-AWSCustomResource',
                          policy=policy,
                          log_retention=log_retention,
                          on_create=on_create, on_update=on_update, on_delete=on_delete,
                          resource_type='Custom::AWS-S3-Object',
                          role=lambda_role,
                          timeout=None)  # Timeout of the Lambda implementing this custom resource. Default: Duration.minutes(2)

    def get_on_create_update(self, bucket_name, object_key, object_content):
        create_params = {
            "Body": object_content,
            "Bucket": bucket_name,
            "Key": object_key,
        }

        # api_version=None uses the latest api
        on_create = AwsSdkCall(
            action='putObject',
            service='S3',
            parameters=create_params,
            # Must keep the same physical resource id, otherwise resource is deleted by CloudFormation
            physical_resource_id=PhysicalResourceId.of(
                f'{bucket_name}/{object_key}'),
        )
        return on_create

    def get_on_delete(self, bucket_name, object_key):
        delete_params = {
            "Bucket": bucket_name,
            "Key": object_key,
        }

        on_delete = AwsSdkCall(
            action='deleteObject',
            service='S3',
            parameters=delete_params,
        )
        return on_delete

    def get_provisioning_lambda_role(self, construct_id: str):
        return iam.Role(
            scope=self,
            id=f'{construct_id}-LambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole")],
        )
