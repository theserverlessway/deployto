import argparse
import yaml
from deployto.deployment.awslambda import LambdaDeployment
from deployto.deployment.elasticbeanstalk import EBDeployment
from deployto import __version__
import traceback

SERVICES = {
    'lambda': LambdaDeployment,
    'elasticbeanstalk': EBDeployment,
}


def main():
    try:
        parser = argparse.ArgumentParser(description='Deploy to various AWS Services.')
        parser.add_argument('--version', action='version', version='{}'.format(__version__))
        parser.add_argument('--config-file', '-c',
                            type=argparse.FileType('r'),
                            help='Set the config files to use', default='deployto.yml')
        args = parser.parse_args()
        config_file = args.config_file.read()
        config = yaml.load(config_file)
        service_id = config.get('service', '')
        if service_id and service_id in SERVICES.keys():
            service = SERVICES[service_id](config)
            service.validate(config)
            service.deploy()
        else:
            print('Service {} is not supported')
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print(type(e).__name__)
