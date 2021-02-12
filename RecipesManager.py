from APIManager import BlizzardAPI
import requests
from ItemManager import Item
from ItemManager import ItemSearch
import json

class RecipeManager:

    def __init__(self, blizz_API : BlizzardAPI = BlizzardAPI()):
        self.access_token = blizz_API.get_access_token()
        self.all_recipes = {}
        self.get_from_file("blacksmithing_recipes")

    def get_from_file(self, file_name):
        with open(file_name) as file:
            data = file.read()

        self.all_recipes = json.loads(data)

    def get_recipe(self, item_name):
        recipe_id = self.all_recipes[item_name]

        url = f"https://us.api.blizzard.com/data/wow/recipe/{recipe_id}?namespace=static-us&locale=en_US&access_token={self.access_token}"
        response = requests.get(url)
        response_json = response.json()

        reagents_json = response_json["reagents"]
        reagents = {}

        for reagent in reagents_json:
            reagents[reagent["reagent"]["name"]] =  reagent["quantity"]

        crafted_quantity = response_json["crafted_quantity"]["value"]

        return crafted_quantity, reagents

    def get_all_recipes(self):
        return self.all_recipes

class RecipeSearch:

    def __init__(self, blizz_API : BlizzardAPI = BlizzardAPI()):
        self.recipe_manager = RecipeManager(blizz_API)
        self.all_recipes = self.recipe_manager.get_all_recipes()

        return

    def search_recipe(self, item : Item, item_search : ItemSearch):

        item_name = item.get_name()
        recipe_id = self.all_recipes[item_name]
        crafted_quantity, reagents_dict = self.recipe_manager.get_recipe(item_name)
        reagents = {}

        for name, quantity in reagents_dict.items():
            new_item = item_search.search_item(name)
            reagents[new_item] = quantity

        item.set_recipe_id(recipe_id)
        item.set_reagents(reagents)
        item.set_crafted_quantity(crafted_quantity)

        return

#r = RecipeManager()
#r.get_from_file("blacksmithing_recipes")
#print(r.all_recipes)
#print(r.get_recipe("Ceremonious Sabatons"))