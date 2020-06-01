import json

from aws_cdk import (
    core,
    aws_s3 as s3
)

from s3_object_custom_resource import S3ObjectResource


class CdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        demo_bucket = s3.Bucket(self,
                                'CustomResourceDemoBucket',
                                versioned=True,
                                block_public_access=s3.BlockPublicAccess.BLOCK_ALL)

        object_content = {
            "somekey": "some_value",
            "somekey2": "some_other_value"
        }

        S3ObjectResource(scope=self, id='S3ObjectResource',
                         bucket_name=demo_bucket.bucket_name,
                         object_key="folder/demo_object.json",
                         object_content=json.dumps(object_content, indent=4))
