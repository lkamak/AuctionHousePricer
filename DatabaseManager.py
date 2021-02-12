import pymongo

"""
Example operations

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]
mydict = {"name": "John", "address": "Highway 37"}
x = mycol.insert_one(mydict)
"""

class DatabaseManager():

    def __init__(self):
        self.db_client = pymongo.MongoClient("mongodb://localhost:27017")

    def create_db(self, db_name: str):
        return self.db_client[db_name]

    def create_collection(self, database, collection_name: str):
        return database[collection_name]

    def write_to_col(self, collection, data):
        return collection.insert_one(data)