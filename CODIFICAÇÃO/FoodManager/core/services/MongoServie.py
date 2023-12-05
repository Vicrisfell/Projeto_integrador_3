import datetime
from core.services.ConnectionService import ConnectionService


class MongoService:
    def __init__(self, conection: ConnectionService, dbname) -> None:
        self.client = conection.getConnection()
        self.db = self.client[dbname]

    def insert(self, collection, **kwargs):
        data = {}
        collection = self.db[collection]
        for key, value in kwargs.items():
            if isinstance(value, datetime.datetime):
                data[key] = value
            elif isinstance(value, datetime.date):
                data[key] = datetime.datetime(value.year, value.month, value.day)
            else:
                data[key] = value

        collection.insert_one(data)

    def find(self, collection, **kwargs):
        collection = self.db[collection]
        return collection.find(kwargs)

    def findOne(self, collection, **kwargs):
        collection = self.db[collection]
        return collection.find_one(kwargs)

    # findAll
    def findAll(self, collection, **kwargs):
        collection = self.db[collection]
        return collection.find(kwargs)

    def delete(self, collection, **kwargs):
        collection = self.db[collection]
        collection.delete_one(kwargs)

    def update(self, collection, filter_query, update_data):
        collection = self.db[collection]
        collection.update_one(filter_query, {"$set": update_data})

    # def update(self, collection, **kwargs):
    #     collection = self.db[collection]
    #     collection.update_one(kwargs)

    # index_with_total
    def index_with_total(self, collection, **kwargs):
        collection = self.db[collection]
        return collection.find(kwargs).count()
