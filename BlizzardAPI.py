import requests
import json
import urllib.parse
import pandas
from config import Config
from requests.auth import HTTPBasicAuth

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

"""
The BlizzardAPI class creates the gateway to search for information directly from the battle.net API. 

The object is initialized and the following methods must be called:
 - get_all_realms
 - get_realm_id
 - get_all_auctions
"""

class BlizzardAPI():

    def __init__(self, region = 'us', realm_name = None):
        client_info = Config()
        self.client_id = client_info.get_client_id()
        self.client_secret = client_info.get_client_secret()
        self.region = region
        self.realm_name = realm_name
        self.access_token = self.create_access_token()
        self.item_list = []
        self.realm_id = 0
        self.all_items = None
        self.all_auctions = None
        self.all_realms = {}

    def create_access_token(self):
        url = "https://%s.battle.net/oauth/token" % self.region
        body = {"grant_type": 'client_credentials'}
        auth = HTTPBasicAuth(self.client_id, self.client_secret)

        response = requests.post(url, data=body, auth=auth)
        print(response)
        return response.json()["access_token"]

    def get_access_tokens(self):
        return {"client_id": self.client_id, "client_secret": self.client_secret}

    def get_all_realms(self):
        url = f"https://us.api.blizzard.com/data/wow/realm/index?namespace=dynamic-us&locale=en_US&access_token={self.access_token}"
        response = requests.get(url)
        response_json = response.json()

        for realm in response_json["realms"]:
            self.all_realms[realm["name"]] = realm["id"]

        self.write_realms_to_file()

    def write_realms_to_file(self):
        with open("realms.txt", "w") as json_file:
            json.dump(self.all_realms, json_file)

    def get_realm_id(self, realm_query):
        self.realm_id = self.all_realms[realm_query]

    def get_item_id(self, item_name):
        item_name_url = urllib.parse.quote(item_name)
        url = f"https://us.api.blizzard.com/data/wow/search/item?namespace=static-us&locale=en_US&name.en_US={item_name_url}&access_token={self.access_token}"
        response = requests.get(url)
        items_dict = response.json()["results"]

        item_id = None

        for item in items_dict:
            if item["data"]["name"]["en_US"] == item_name:
                item_id = item["data"]["id"]

        return item_id

    def is_stackable(self, item_id):
        url = f"https://us.api.blizzard.com/data/wow/item/{item_id}?namespace=static-us&locale=en_US&access_token={self.access_token}"
        response = requests.get(url)
        stackable = response.json()["is_stackable"]
        return stackable

    def get_all_auctions(self):
        url = f"https://us.api.blizzard.com/data/wow/connected-realm/{self.realm_id}/auctions?namespace=dynamic-us&locale=en_US&access_token={self.access_token}"
        response = requests.get(url)
        self.all_auctions = response.json()["auctions"]

    def get_item_price(self, item_id):

        min_cost = float('inf')

        for auction in self.all_auctions:
            if auction["item"]["id"] == item_id:
                if self.is_stackable(item_id):
                    if auction["unit_price"] < min_cost:
                        min_cost = auction["unit_price"]
                else:
                    if auction["buyout"] < min_cost:
                        min_cost = auction["buyout"]

        return min_cost / 10000

#blizzAPI = BlizzardAPI(myclient_id, myclient_secret, 'us')
#blizzAPI.get_all_realms()
#blizzAPI.get_realm_id("Illidan")
#blizzAPI.get_all_auctions()
#abyssal_id = blizzAPI.get_item_id("Sky Golem")

#print(blizzAPI.all_realms['Illidan'])
#print(blizzAPI.get_item_price(abyssal_id))
#print(blizzAPI.realm_id)


