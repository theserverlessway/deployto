import boto3

client = boto3.client('cloudformation')


class StackResourceException(Exception):
    def __init__(self, resource_type):
        message = 'Please select a single {} to use for deployment'
        super(StackResourceException, self).__init__(message.format(resource_type))


class StackResources():
    def __init__(self, stackName):
        self.resources = client.list_stack_resources(StackName=stackName)['StackResourceSummaries']

    def filter(self, resource_type, logicalIds):
        resources = list(filter(lambda x: x['ResourceType'] == resource_type and
                                (not logicalIds or x['LogicalResourceId'] in logicalIds), self.resources))

        return list(map(lambda x: x['PhysicalResourceId'], resources))

    def single(self, resource_type, logicalId):
        resources = self.filter(resource_type, logicalId)
        if len(resources) != 1:
            raise StackResourceException(resource_type)
        else:
            return resources[0]
