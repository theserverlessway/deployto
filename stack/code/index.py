from datetime import datetime


def handler(event, context):
    return datetime.now().isoformat()
