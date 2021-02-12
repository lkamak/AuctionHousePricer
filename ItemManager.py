from APIManager import BlizzardAPI
import requests
import urllib.parse
import json

class Item:

    def __init__(self, name):
        self.id = ""
        self.name = name
        self.profession_name = ""
        self.profession_id = ""
        self.recipe_id = ""
        self.is_stackable = None
        self.vendor_price = 0
        self.auction_price = 0
        self.reagents = {}
        self.crafted_quantity = 0
        self.total_cost = 0

    def show_all_info(self):
        print(f"Item ID: {self.id}")
        print(f"Item Name: {self.name}")
        print(f"Profession Name: {self.profession_name}")
        print(f"Profession ID: {self.profession_id}")
        print(f"Recipe ID: {self.recipe_id}")
        print(f"Is Stackable: {self.is_stackable}")
        print(f"Vendor Price: {self.vendor_price}")
        print(f"Auction Price: {self.auction_price}")
        print("Reagents:")
        for item, quantity in self.reagents.items():
            print(f"  {item.get_name()} : {quantity}")
        print(f"Crafted Quantity: {self.crafted_quantity}")
        print(f"Total Cost: {self.total_cost}")
        print(f"Gross Profit: {(  self.auction_price * self.crafted_quantity) - self.total_cost}")

    def set_id(self, id:str):
        self.id = id

    def set_profession_name(self, profession_name : str):
        self.profession_name = profession_name

    def set_profession_id(self, profession_id : str):
        self.profession_id = profession_id

    def set_recipe_id(self, recipe_id : str):
        self.recipe_id = recipe_id

    def set_stackable(self, stackable : bool):
        self.is_stackable = stackable

    def set_vendor_price(self, vendor_price : int):
        self.vendor_price = vendor_price

    def set_auction_price(self, auction_price : int):
        self.auction_price = auction_price

    def set_reagents(self, reagents : {}):
        self.reagents = reagents

    def set_crafted_quantity(self, quantity : int):
        self.crafted_quantity = quantity

    def set_total_cost(self, cost):
        self.total_cost = cost

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_profession_name(self):
        return self.profession_name

    def get_profession_id(self):
        return self.profession_id

    def get_recipe_id(self):
        return self.recipe_id

    def get_stackable(self):
        return self.is_stackable

    def get_vendor_price(self):
        return self.vendor_price

    def get_auction_price(self):
        return self.auction_price

    def get_reagents(self):
        return self.reagents

    def get_crafted_quantity(self):
        return self.crafted_quantity

    def get_total_cost(self):
        return self.total_cost

    def get_profit(self):
        return self.auction_price - self.total_cost

class ItemSearch:

    def __init__(self, blizzAPI:BlizzardAPI = BlizzardAPI()):
        self.access_token = blizzAPI.get_access_token()
        self.searchCache = []

    def search_item(self, item_name):
        new_item = Item(item_name)

        item_name_url = urllib.parse.quote(item_name)
        url = f"https://us.api.blizzard.com/data/wow/search/item?namespace=static-us&locale=en_US&name.en_US={item_name_url}&access_token={self.access_token}"
        response = requests.get(url)

        items_dict = response.json()["results"]

        for item in items_dict:
            if item["data"]["name"]["en_US"] == item_name:
                new_item.set_id(item["data"]["id"])
                new_item.set_stackable(item["data"]["is_stackable"])
                new_item.set_vendor_price(item["data"]["purchase_price"])

        return new_item

#newItemSearch = ItemSearch()
#newItem = newItemSearch.search_item("Shadowghast Ingot")
#newItem.show_all_info()

