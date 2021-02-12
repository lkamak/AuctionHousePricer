"""
Config file with necessary credentials to run api
"""

class Config():

    def __init__(self):
        self.client_id = "f5eae9efac6542f8b00653232cd9bc0c"
        self.client_secret = "ErRyVvsli5MvtpYp8Xg2aHcqL1i8EtC3"

    def get_client_id(self):
        return self.client_id

    def get_client_secret(self):
        return self.client_secret

    def update_client_id(self, client_id):
        self.client_id = client_id
        pass

    def update_client_secret(self, client_secret):
        self.client_secret = client_secret
        pass

