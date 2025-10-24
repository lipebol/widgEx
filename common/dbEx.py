from .loadEx import load, system
from pymongo import MongoClient
from pymongoarrow.monkey import patch_all

class mongodb:

    @staticmethod
    def connect(database: str, collection: str):
        patch_all()
        return MongoClient(
            system.decr(value=load.variable('MONGODB_URI'))
        ).get_database(
            database if database else load.variable('MONGODB_DEFAULT')
        ).get_collection(collection)

    @staticmethod
    def select(
        collection: str, *, database: str | None = None, 
        filter: dict = {}, fields: dict = {}, _id: str | bool = False
    ) -> list:
        _db = mongodb.connect(database, collection)
        if not filter and not _id:
            return _db.find_arrow_all({}).drop_columns('_id').to_pylist()
        return list(_db.find(filter, fields))

    @staticmethod
    def update(collection: str, *, filter: dict, update: dict, database: str | None = None):
        return mongodb.connect(database, collection).update_many(filter, { '$set' : update})

    @staticmethod
    def setdb(database: str):
        load.variable('MONGODB_DEFAULT', add=database)
    


    