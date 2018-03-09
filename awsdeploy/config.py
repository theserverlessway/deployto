from schematics.models import Model
from schematics.types import StringType, BooleanType


class Config(Model):
    stack = StringType(required=True)
    service = StringType(required=True, choices=['lambda', 'elasticbeanstalk'])
    s3 = BooleanType(default=False)
