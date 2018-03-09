from schematics.models import Model
from schematics.types import StringType


class Config(Model):
    stack = StringType(required=True)
    service = StringType(required=True, choices=['lambda', 'elasticbeanstalk'])
