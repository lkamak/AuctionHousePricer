from ItemManager import Item
from APIManager import BlizzardAPI
import requests
import json

class AuctionHouseManager:

    def __init__(self, realm_id : int, blizz_API : BlizzardAPI):
        self.access_token = blizz_API.get_access_token()
        self.realm_id = realm_id
        self.vendor_items = {"Luminous Flux":5}
        self.all_auctions = self.get_all_auctions()

    def get_all_auctions(self):
        url = f"https://us.api.blizzard.com/data/wow/connected-realm/{self.realm_id}/auctions?namespace=dynamic-us&locale=en_US&access_token={self.access_token}"
        response = requests.get(url)
        return response.json()["auctions"]

    def get_item_price(self, item : Item):
        min_cost = float('inf')

        for auction in self.all_auctions:
            if auction["item"]["id"] == item.get_id():
                if item.get_stackable():
                    if auction["unit_price"] < min_cost:
                        min_cost = auction["unit_price"]
                else:
                    if auction["buyout"] < min_cost:
                        min_cost = auction["buyout"]

        item.set_auction_price(min_cost / 10000)
        return min_cost / 10000

    def get_item_cost(self, item : Item):

        item_cost = 0

        for reagent, quantity in item.get_reagents().items():

            reagent_name = reagent.get_name()

            if reagent_name in self.vendor_items:
                reagent_price = self.vendor_items[reagent_name]
            else:
                reagent_price = self.get_item_price(reagent)

            print(f"{reagent_name} : {reagent_price}")
            item_cost += reagent_price * quantity

        item.set_total_cost(item_cost)
        return item_cost

#newAPI = BlizzardAPI()
#newAuction = AuctionHouseManager(57, newAPI)
#print(newAuction.all_auctions)