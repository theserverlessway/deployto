# File needs to be named awslambda.py as python doesn't accept just lambda in imports
import boto3
import uuid
from deployto.deployment.base import BaseDeployment
from deployto.config import Config
from schematics.types import ListType, StringType, BooleanType
from deployto import package

client = boto3.client('cloudformation')
awslambda = boto3.client('lambda')


class LambdaDeployment(BaseDeployment):
    def __init__(self, config):
        super(LambdaDeployment, self).__init__(LambdaConfig(config))

    def deploy(self):
        zipfile = package.package(self.config.paths)
        try:
            update_arguments = {}

            if self.config.s3:
                s3 = boto3.client('s3')
                bucket_name = 'deploy-{}'.format(str(uuid.uuid4()).lower())
                bucket_path = 'deployment.zip'
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration=dict(LocationConstraint=boto3.session.Session().region_name)
                )
                s3.put_object(Bucket=bucket_name, Key=bucket_path, Body=zipfile)
                update_arguments = dict(S3Bucket=bucket_name, S3Key=bucket_path)
            else:
                update_arguments = dict(ZipFile=zipfile)

            functions = list(filter
                             (lambda x: x['ResourceType'] == 'AWS::Lambda::Function',
                              client.list_stack_resources(StackName=self.config.stack)['StackResourceSummaries']))

            if self.config.functions:
                functions = list(filter(lambda x: x['LogicalResourceId'] in self.config.functions, functions))

            if functions:
                for function in functions:
                    awslambda.update_function_code(
                        FunctionName=function['PhysicalResourceId'], Publish=self.config.publish, **update_arguments)
                    print('Function {} deployed successfully'.format(function['LogicalResourceId']))
            else:
                print('No Functions selected for deployment')

        except Exception as e:
            print(e)
        finally:
            if self.config.s3:
                s3.delete_object(Bucket=bucket_name, Key=bucket_path)
                s3.delete_bucket(Bucket=bucket_name)


class LambdaConfig(Config):
    functions = ListType(StringType, default=[])
    paths = ListType(StringType, default=['./'])
    publish = BooleanType(default=False)
    s3 = BooleanType(default=False)
