from APIManager import BlizzardAPI
from RecipesManager import RecipeSearch
from RecipesManager import RecipeManager
from ItemManager import Item
from ItemManager import ItemSearch
from AuctionHouseManager import AuctionHouseManager
import json

class Search:

    def __init__(self, realm_name, blizzAPI:BlizzardAPI = BlizzardAPI()):
        with open("realms.txt") as file:
            data = file.read()

        realm_id = json.loads(data)[realm_name]

        self.item_search = ItemSearch(blizzAPI)
        self.recipe_search = RecipeSearch(blizzAPI)
        self.auction_house = AuctionHouseManager(realm_id, blizzAPI)

        self.searchCache = []

    def search(self, item_name):

        item = self.item_search.search_item(item_name)
        self.recipe_search.search_recipe(item, self.item_search)
        self.auction_house.get_item_price(item)
        self.auction_house.get_item_cost(item)

        return item

newAPI = BlizzardAPI()
newSearch = Search("Illidan", newAPI)
newItem = newSearch.search("Shadowsteel Breastplate")
newItem.show_all_info()
