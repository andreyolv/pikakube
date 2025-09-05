from pymongo import MongoClient
from faker import Faker

class MongoGen:
    def __init__(self, host, user, password, database):
        self.client = MongoClient(host, 27017, username=user, password=password)
        self.database = client[database]

    def create_collection(self, collection):
        if collection in self.database.list_collection_names():
            print(f"Collection '{collection}' already exists.")
        else:
            self.database.create_collection(collection)
            print(f"Collection '{collection}' created!")

    def insert_data(self, collection, fields, quantity):
        collection = self.database[collection]
        fake = Faker()
                
        for _ in range(quantity):
            document = {}
            for field in fields:
                document[field] = getattr(fake, field)()

            collection.insert_one(document)

    def drop_collection(self, collection):
        if collection in self.database.list_collection_names():
            self.database[collection].drop()
            print(f"Collection '{collection}' deleted successfully.")
        else:
            print(f"Collection '{collection}' not exists.")