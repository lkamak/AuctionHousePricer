from APIManager import BlizzardAPI
import requests
import json

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

class ProfessionsSetUp:

    def __init__(self):
        blizzAPI = BlizzardAPI()
        self.access_token = blizzAPI.get_access_token()
        self.all_professions = {}
        self.all_sub_professions = {}
        self.all_skill_tiers = None
        self.all_recipes = {}

    def get_all_professions(self):
        url = f"https://us.api.blizzard.com/data/wow/profession/index?namespace=static-us&locale=en_US&access_token={self.access_token}"
        response = requests.get(url)
        response_json = response.json()

        for profession in response_json["professions"]:
            self.all_professions[profession["name"]] = profession["id"]

    def get_all_subprofessions(self, profession_id):
        url = f"https://us.api.blizzard.com/data/wow/profession/{profession_id}?namespace=static-us&locale=en_US&access_token={self.access_token}"
        response = requests.get(url)
        response_json = response.json()

        for subprofession in response_json["skill_tiers"]:
            self.all_sub_professions[subprofession["name"]] = subprofession["id"]

    def get_all_skill_tiers(self, profession_id, sub_profession_id):
        url = f"https://us.api.blizzard.com/data/wow/profession/{profession_id}/skill-tier/{sub_profession_id}?namespace=static-us&locale=en_US&access_token={self.access_token}"
        response = requests.get(url)
        response_json = response.json()
        self.all_skill_tiers = response_json

    def get_all_recipes(self):

        for category in self.all_skill_tiers["categories"]:
            for recipe in category["recipes"]:
                self.all_recipes[recipe["name"]] = recipe["id"]

    def write_to_file(self, file, data):
        with open(file, "w") as json_file:
            json.dump(data, json_file)

profsetup = ProfessionsSetUp()
profsetup.get_all_professions()
profsetup.get_all_subprofessions("164")
profsetup.write_to_file("subprofessions.txt", profsetup.all_sub_professions)
profsetup.get_all_skill_tiers("164", "2751")
profsetup.get_all_recipes()
profsetup.write_to_file("blacksmithing_recipes", profsetup.all_recipes)
print(profsetup.all_recipes)






