import requests
import json
import urllib.parse
import pandas
from requests.auth import HTTPBasicAuth

myclient_id = "f5eae9efac6542f8b00653232cd9bc0c"
myclient_secret = "uA2J3dfIFhjh9JvaY42KX4ETNRsF4MGj"

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

class BlizzardAPI():

    def __init__(self, client_id, client_secret, region = 'us'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region
        self.access_token = self.create_access_token()
        self.item_list = []
        self.realm_id = 0
        self.all_items = None
        self.all_auctions = None

    def create_access_token(self):
        url = "https://%s.battle.net/oauth/token" % self.region
        body = {"grant_type": 'client_credentials'}
        auth = HTTPBasicAuth(self.client_id, self.client_secret)

        response = requests.post(url, data=body, auth=auth)
        print(response)
        return response.json()["access_token"]

    def get_realm_id(self, realm_query):
        realm_name_url = urllib.parse.quote(realm_query)
        url = f"https://us.api.blizzard.com/data/wow/realm/{realm_name_url}?namespace=dynamic-us&locale=en_US&access_token={self.access_token}"
        response = requests.get(url)
        self.realm_id = response.json()["id"]

    def get_item_id(self, item_name):
        item_name_url = urllib.parse.quote(item_name)
        url = f"https://us.api.blizzard.com/data/wow/search/item?namespace=static-us&locale=en_US&name.en_US={item_name_url}&access_token={self.access_token}"
        response = requests.get(url)
        items_dict = response.json()["results"]

        item_id = None

        for item in items_dict:
            if item["data"]["name"]["en_US"] == item_name:
                item_id = item["data"]["id"]

        print(item_id)
        return item_id

    def get_all_auctions(self):
        url = f"https://us.api.blizzard.com/data/wow/connected-realm/{self.realm_id}/auctions?namespace=dynamic-us&locale=en_US&access_token={self.access_token}"
        response = requests.get(url)
        self.all_auctions = response.json()["auctions"]

    def get_item_price(self, item_id):

        min_cost = float('inf')

        for auction in self.all_auctions:
            if auction["item"]["id"] == item_id:
                if auction["unit_price"] < min_cost:
                    min_cost = auction["unit_price"]

        return min_cost / 10000

blizzAPI = BlizzardAPI(myclient_id, myclient_secret, 'us')
blizzAPI.get_realm_id("illidan")
blizzAPI.get_all_auctions()
abyssal_id = blizzAPI.get_item_id("Shadestone")

print(blizzAPI.get_item_price(abyssal_id))
print(blizzAPI.realm_id)


