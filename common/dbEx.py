from .addEx import add
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
    def update(collection: str, *, database: str | None = None, filter: dict, update: dict):
        return mongodb.connect(database, collection).update_many(filter, { '$set' : update})

    @staticmethod
    def insert(
        collection: str, *, database: str | None = None, 
        data: dict, many: bool = False
    ):
        if not many:
            return mongodb.connect(database, collection).insert_one(data).inserted_id

    @add.exception
    @staticmethod
    def setconfig(database: str | None = None):
        if database:
            load.variable('MONGODB_DEFAULT', add=database)
            return list(mongodb().__env)

    @property
    def __env(self):
        if not load.checkpath(tmpfile := load.tmpfile(path='/tmp')):
            load.jsonEx(path=tmpfile, data=mongodb.select('_envs', database='common')[0])
        for key, value in load.jsonEx(path=tmpfile).items():
            yield load.variable(key, add=value)
    


    