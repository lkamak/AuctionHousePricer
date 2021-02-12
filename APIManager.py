import requests
import json
from config import Config
from requests.auth import HTTPBasicAuth

class BlizzardAPI():

    def __init__(self, region = 'us'):
        client_info = Config()
        self.client_id = client_info.get_client_id()
        self.client_secret = client_info.get_client_secret()
        self.region = region
        self.access_token = ""
        self.create_access_token()

    def create_access_token(self):
        url = "https://%s.battle.net/oauth/token" % self.region
        body = {"grant_type": 'client_credentials'}
        auth = HTTPBasicAuth(self.client_id, self.client_secret)

        response = requests.post(url, data=body, auth=auth)
        print(response)

        access_token = response.json()["access_token"]
        self.access_token = access_token

    def get_credentials(self):
        return {"client_id": self.client_id, "client_secret": self.client_secret}

    def get_access_token(self):
        return self.access_token
