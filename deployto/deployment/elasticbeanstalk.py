import boto3
from deployto.deployment.base import BaseDeployment
from deployto.config import Config
from schematics.types import ListType, StringType
from deployto import package
from deployto.resources import StackResources
from datetime import datetime
from time import sleep

elasticbeanstalk = boto3.client('elasticbeanstalk')
s3 = boto3.client('s3')

class EBDeploymentException(Exception):
    pass


VERSION_PROCESSING_SUCCESS = 'PROCESSED'
VERSION_PROCESSING_FAILED = 'FAILED'

VERSION_PROCESSING_FINISHED = [VERSION_PROCESSING_SUCCESS, VERSION_PROCESSING_FAILED]

ENVIRONMENT_READY_STATUS = 'READY'

class EBDeployment(BaseDeployment):
    def __init__(self, config):
        super(EBDeployment, self).__init__(EBDeploymentConfig(config))

    def deploy(self):
        zipfile = package.package(self.config.paths)

        stack_resources = StackResources(self.config.stack)

        bucket_name = stack_resources.single('AWS::S3::Bucket', self.config.bucket)

        timestamp = datetime.now().isoformat()

        bucket_path = '{}-{}-deployment.zip'.format(self.config.stack, timestamp)

        s3.put_object(Bucket=bucket_name, Key=bucket_path, Body=zipfile)

        app_version = "{}-{}".format(self.config.stack, timestamp)

        application = stack_resources.single('AWS::ElasticBeanstalk::Application', self.config.application)

        environment = stack_resources.single('AWS::ElasticBeanstalk::Environment', self.config.environment)

        print('Creating Application Version {}'.format(app_version))
        elasticbeanstalk.create_application_version(
            ApplicationName=application,
            VersionLabel=app_version,
            SourceBundle=dict(S3Bucket=bucket_name, S3Key=bucket_path),
            Process=True
        )

        print('Waiting for Version to be processed', end='', flush=True)
        while self.version_status(application, app_version) not in VERSION_PROCESSING_FINISHED:
            sleep(3)
            print('.', end='', flush=True)

        if self.version_status(application, app_version) == VERSION_PROCESSING_FAILED:
            raise EBDeploymentException('Failed to process Application Version {}'.format(app_version))

        print('')

        print('Updating Environment')
        elasticbeanstalk.update_environment(
            ApplicationName=application,
            EnvironmentName=environment,
            VersionLabel=app_version
        )

        print('Waiting for Update to finish', end='', flush=True)
        while self.environment(application, environment)['Status'].upper() != ENVIRONMENT_READY_STATUS:
            sleep(5)
            print('.', end='', flush=True)

        print('')

        if self.environment(application, environment)['Health'] == 'Green':
            print('Deployed to {}:{} successfully'.format(application, environment))
        else:
            raise EBDeploymentException('Deployment Failed to {}:{}'.format(application, environment))

    def version_status(self, application, version):
        status = elasticbeanstalk.describe_application_versions(
            ApplicationName=application,
            VersionLabels=[version]
        )['ApplicationVersions'][0]['Status']
        return status.upper()

    def environment(self, application, environment):
        return elasticbeanstalk.describe_environments(
            ApplicationName=application,
            EnvironmentNames=[
                environment
            ]
        )['Environments'][0]


class EBDeploymentConfig(Config):
    environment = StringType(default='')
    application = StringType(default='')
    paths = ListType(StringType, default=['./'])
    bucket = StringType('')
