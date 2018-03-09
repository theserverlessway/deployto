import argparse
import yaml
from awsdeploy.deployment.awslambda import LambdaDeployment
from awsdeploy import __version__

SERVICES = {
    'lambda': LambdaDeployment,
}


def main():
    try:
        parser = argparse.ArgumentParser(description='Deploy to various AWS Services.')
        parser.add_argument('--version', action='version', version='{}'.format(__version__))
        parser.add_argument('--config-file', '-c',
                            type=argparse.FileType('r'),
                            help='Set the config files to use', default='awsdeploy.yaml')
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
        print(type(e).__name__)
