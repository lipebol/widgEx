from .addEx import add
from .loadEx import load, system
import adbc_driver_postgresql.dbapi
from pymongo import MongoClient
from pymongoarrow.monkey import patch_all


class postgresql:
 
    @staticmethod
    def __connect(database):
        if (database := database or load.variable('POSTGRESQL_DEFAULT')):
            return adbc_driver_postgresql.dbapi.connect(
                system.decr(value=load.variable('POSTGRESQL_URI')) % 
                {'db': database}, autocommit=True
            ).cursor()
        raise Exception('The database was not declared.')
    
    @staticmethod
    def columns(*, schema: str, table: str, database: str | None = None) -> list:
        if schema and table:
            with postgresql.__connect(database) as conn:
                conn.execute(load.variable('SELECT_COMMAND') % (schema,table,''))
                return [column[0] for column in conn.description]

    @staticmethod
    def select(
        *, schema: str, table: str, params='', 
        database: str | None = None
    ):
        if schema and table:
            with postgresql.__connect(database) as conn:
                conn.execute(load.variable('SELECT_COMMAND') % (schema,table,params))
                return conn.fetch_arrow_table()

    @staticmethod
    def adbc(
        *, data: object, schema: str, table: str, 
        database: str | None = None
    ):
        if data and schema and table:
            with postgresql.__connect(database) as conn:
                conn.adbc_ingest(
                    db_schema_name=schema, table_name=table, 
                    data=data, mode='append'
                )
            return postgresql.select(schema, table)

    @add.exception
    @staticmethod
    def setconfig(database: str | None = None):
        config.db('POSTGRESQL_DEFAULT', database)
        return list(config.envs())


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
        config.db('MONGODB_DEFAULT', database)
        return list(config.envs())


class config:

    @staticmethod
    def db(env: str, database: str | None = None) -> list:
        if database:
            return load.variable(env, add=database)

    @staticmethod
    def envs():
        if not load.checkpath(tmpfile := load.tmpfile(path='/tmp')):
            load.jsonEx(path=tmpfile, data=mongodb.select('_envs', database='common')[0])
        for key, value in load.jsonEx(path=tmpfile).items():
            yield load.variable(key, add=value)