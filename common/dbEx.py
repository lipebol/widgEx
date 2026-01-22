from .authEx import auth
from .loadEx import load, system
from .notifEx import notific
import adbc_driver_postgresql.dbapi
from pymongo import MongoClient
from pymongoarrow.monkey import patch_all


class ClickHouse:

    @staticmethod
    def setconfig(database: str | None = None):
        config.setdbname('CLICKHOUSE_DB', database)
        return config.envs()

    @staticmethod
    def getdbname(database: str | None) -> str:
        if (database := database or load.variable('CLICKHOUSE_DB')):
            return database
        raise Exception('The database was not declared.')

    @staticmethod
    def __connect(database: str | None, **kwargs):
        if kwargs.get('query') and kwargs.get('table'):
            raise Exception('Choose one of the two methods: "query" or "table".')
        elif kwargs.get('table'):
            kwargs['default'] = ClickHouse.getdbname(database) ### <-- to env 'SELECT_ALL'
        return auth.arrowflightrpc(load.variable('CLICKHOUSE_URI'), **kwargs)
        
    @staticmethod
    def select(*, database: str | None = None, **kwargs):
        if kwargs.get('query') or kwargs.get('table'):
            if (flight := ClickHouse.__connect(database, **kwargs)):
                if not flight.info.rows:
                    return flight.info.schema.empty_table()
                return flight.conn.client.do_get(
                    flight.info.ticket, flight.conn.authenticate
                ).read_all()
        raise Exception('The "query" or "table" was not declared.')

    @staticmethod
    def insert(*, database: str | None = None, **kwargs):
        if (table := kwargs.get('table')):
            config = {'insert_path': True, **kwargs}
            if (flight := ClickHouse.__connect(database, **config)):
                if (schema := kwargs.get('use_schema')):
                    flight.info.schema = schema
                writer, _ = flight.conn.client.do_put(
                    flight.conn.descriptor.for_path(flight.extras.path), 
                    flight.info.schema, flight.conn.authenticate
                )
                return writer
        raise Exception('The "table" was not declared.')

    @staticmethod
    def info(*, database: str | None = None, **kwargs):
        if kwargs.get('query') or kwargs.get('table'):
            config = {'info': True, **kwargs}
            return ClickHouse.__connect(database, **config)
        raise Exception('The "query" or "table" was not declared.')


class PostgreSQL:

    @staticmethod
    def setconfig(database: str | None = None):
        config.setdbname('POSTGRESQL_DB', database)
        return config.envs()

    @staticmethod
    def getdbname(database: str | None) -> str:
        if (database := database or load.variable('POSTGRESQL_DB')):
            return database
        raise Exception('The database was not declared.')

    @staticmethod
    def __connect(database: str | None):
        return adbc_driver_postgresql.dbapi.connect(
            system.decr(value=load.variable('POSTGRESQL_URI')) % 
            {'db': config.getdbname(database)}, autocommit=True
        ).cursor()

    @staticmethod
    def select(
        schema: str, *,  table: str, params: str = '', 
        database: str | None = None
    ):
        if schema and table:
            with PostgreSQL.__connect(database) as conn:
                conn.execute(load.variable('SELECT_ALL') % (f"{schema}.{table}",params))
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
            with PostgreSQL.__connect(database) as conn:
                conn.adbc_ingest(
                    db_schema_name=schema, table_name=table, 
                    data=data, mode='append'
                )
            load.info(f"Inserted {rows} rows in {schema}.{table}")
            if return_id:
                return PostgreSQL.select(
                    schema, table=table, 
                    params="WHERE id IN (%s)" % ",".join(
                        [f"'{id}'" for id in data.select(["id"]).to_pydict()['id']]
                    )
                )
            return None
        load.info("No data was found to insert.")

    @staticmethod
    def columns(schema: str, *, table: str, database: str | None = None) -> list:
        if schema and table:
            with PostgreSQL.__connect(database) as conn:
                conn.execute(load.variable('SELECT_ALL') % (schema,table,''))
                return [column[0] for column in conn.description]

    @staticmethod
    def sizedb(target: str, *, database: str | None = None):
        if len((target := target.lower().split())) == 2:
            with PostgreSQL.__connect(database) as conn:
                conn.execute(load.variable('SIZEDB') % PostgreSQL.getdbname(database))
                if (sizedb := "".join(conn.fetchone()).lower().split()):
                    load.info(sizedb)
                    if target[1] == sizedb[1] and int(target[0]) <= int(sizedb[0]):
                        raise Exception('The specified target was hit.')
                return True
        raise Exception('Please specify the desired limit in the format: <size> <unit>')


class MongoDB:

    patch_all()

    @staticmethod
    def setconfig(database: str | None = None):
        config.setdbname('MONGODB_DB', database)
        return config.envs()

    @staticmethod
    def getdbname(database: str | None) -> str:
        if (database := database or load.variable('MONGODB_DB')):
            return database
        raise Exception('The database was not declared.')

    @staticmethod
    def connect(database: str, collection: str):
        return MongoClient(
            system.decr(value=load.variable('MONGODB_URI'))
        ).get_database(MongoDB.getdbname(database)).get_collection(collection)

    @staticmethod
    def select(
        collection: str, *, database: str | None = None, 
        filter: dict = {}, fields: dict = {}, _id: bool = False
    ) -> list:
        _db = MongoDB.connect(database, collection)
        if not filter:
            if (data := _db.find_arrow_all({})):
                return data.drop_columns('_id') if not _id else data
        return list(_db.find(filter, fields))

    @staticmethod
    def update(collection: str, *, database: str | None = None, filter: dict, update: dict):
        return MongoDB.connect(database, collection).update_many(filter, { '$set' : update})

    @staticmethod
    def insert(
        collection: str, *, database: str | None = None, 
        data: dict, many: bool = False
    ):
        if not many:
            return MongoDB.connect(database, collection).insert_one(data).inserted_id
    

class config:

    @staticmethod
    def setdbname(env: str, database: str | None) -> list:
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
        if (dataenv := MongoDB.select('_envs', database='common').to_pylist()):
            load.jsonEx(path=tmpfile, data=dataenv[0])
            return list(load.envs())
        raise Exception('Error load envs.')