class Deployment():
    def __init__(self, config):
        self.config = config

    def validate(self, config):
        self.config.validate()
