from .authEx import auth
from .loadEx import load, system
from .notifEx import notific
import adbc_driver_postgresql.dbapi
from pymongo import MongoClient
from pymongoarrow.monkey import patch_all


class clickhouse:

    @staticmethod
    def __connect(**kwargs):
        return auth.arrowflightrpc(load.variable('CLICKHOUSE_URI'), **kwargs)

    @staticmethod
    def select(command: str):
        if (flight := clickhouse.__connect(command=command)):
            flight.conn.descriptor = flight.conn.descriptor.for_command(command)
            return flight

    @staticmethod
    def insert(path: str):
        if (flight := clickhouse.__connect(path=path)):
            flight.conn.descriptor = flight.conn.descriptor.for_path(path)
            return flight

    @staticmethod
    def info(command: str):
        if (flight := clickhouse.__connect(command=command,info=True)):
            return flight


class postgresql:
 
    @staticmethod
    def __connect(database: str | None):
        return adbc_driver_postgresql.dbapi.connect(
            system.decr(value=load.variable('POSTGRESQL_URI')) % 
            {'db': postgresql.isdb(database)}, autocommit=True
        ).cursor()

    @staticmethod
    def sizedb(target: str, *, database: str | None = None):
        if len((target := target.lower().split())) == 2:
            with postgresql.__connect(
                (database := postgresql.isdb(database))
            ) as conn:
                conn.execute(load.variable('SIZEDB') % database)
                if (sizedb := "".join(conn.fetchone()).lower().split()):
                    load.info(sizedb)
                    if target[1] == sizedb[1] and int(target[0]) <= int(sizedb[0]):
                        raise Exception('The specified target was hit.')
                return True
        raise Exception('Please specify the desired limit in the format: <size> <unit>')
    
    @staticmethod
    def isdb(database: str | None) -> str:
        if (database := database or load.variable('POSTGRESQL_DB')):
            return database
        raise Exception('The database was not declared.')
    
    @staticmethod
    def columns(schema: str, *, table: str, database: str | None = None) -> list:
        if schema and table:
            with postgresql.__connect(database) as conn:
                conn.execute(load.variable('SELECT') % (schema,table,''))
                return [column[0] for column in conn.description]

    @staticmethod
    def select(
        schema: str, *,  table: str, params='', 
        database: str | None = None
    ):
        if schema and table:
            with postgresql.__connect(database) as conn:
                conn.execute(load.variable('SELECT') % (f"{schema}.{table}",params))
                return conn.fetch_arrow_table()

    @staticmethod
    def insert(
        schema: str, *, table: str, data: object,
        return_id: bool = True, database: str | None = None
    ):
        if data and schema and table:
            if 'pyarrow.lib.Table' not in str(type(data)):
                data, rows = data.to_batches(), data.count_rows()
            else:
                rows = data.num_rows
            with postgresql.__connect(database) as conn:
                conn.adbc_ingest(
                    db_schema_name=schema, table_name=table, 
                    data=data, mode='append'
                )
            load.info(f"Inserted {rows} rows in {schema}.{table}")
            if return_id:
                return postgresql.select(
                    schema, table=table, 
                    params="WHERE id IN (%s)" % ",".join(
                        [f"'{id}'" for id in data.select(["id"]).to_pydict()['id']]
                    )
                )
            return None
        load.info("No data was found to insert.")

    @staticmethod
    def setconfig(database: str | None = None):
        config.db('POSTGRESQL_DB', database)
        return config.envs()


class mongodb:

    @staticmethod
    def connect(database: str, collection: str):
        patch_all()
        return MongoClient(
            system.decr(value=load.variable('MONGODB_URI'))
        ).get_database(
            database if database else load.variable('MONGODB_DB')
        ).get_collection(collection)

    @staticmethod
    def select(
        collection: str, *, database: str | None = None, 
        filter: dict = {}, fields: dict = {}, _id: bool = False
    ) -> list:
        _db = mongodb.connect(database, collection)
        if not filter:
            if (data := _db.find_arrow_all({})):
                return data.drop_columns('_id') if not _id else data
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
    
    @load.quiet
    @staticmethod
    def setconfig(database: str | None = None):
        config.db('MONGODB_DB', database)
        return config.envs()


class config:

    @staticmethod
    def db(env: str, database: str | None = None) -> list:
        if database:
            return load.variable(env, add=database)

    @notific.exception
    @staticmethod
    def envs():
        if load.checkpath(tmpfile := load.tmpfile(path='/tmp')):
            if not (envs := list(load.envs())):
                if load.checkpath(tmpfile):
                    raise Exception(error)
            else:
                return envs
        if (dataenv := mongodb.select('_envs', database='common').to_pylist()):
            load.jsonEx(path=tmpfile, data=dataenv[0])
            return list(load.envs())
        raise Exception('Error load envs.')