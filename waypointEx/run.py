from common.dbEx import postgresql
from common.httpEx import httpEx
from common.loadEx import load, system
from common.mountEx import mount
from common.notifEx import notific
from fsspec import filesystem
import pyarrow as arrow
from time import sleep
from xmltodict import parse

class init:

    @staticmethod
    def to_table(data: list) -> object:
        def parser(content: str|tuple) -> dict:
            if 'Contents' in str(content):
                content = [
                    str(value.strip('"')) 
                    for key, value in parse(content.encode()).get('Contents').items() 
                    if key in ('Key','LastModified','ETag','Size')
                ]
            return dict(zip(['filename','last_modified','id','size'], content))
        return arrow.Table.from_pylist(list(map(parser, data)))

    @staticmethod
    def columns_types():
        if (columns := postgresql.columns(load.schemadb(), table= 'gte_2020')):
            return [
                (column, arrow.string()) if column not in ('started_at','ended_at') 
                else (column, arrow.timestamp('ms')) for column in columns 
                if column not in ('id')
            ]

    @staticmethod
    def dataload():
        newfiles = init.to_table(
            httpEx.scrape(url=(url := load.variable('DIVVYBIKES')), type='xml', tag='Contents')
        ).join(
            postgresql.select((schema := load.schemadb()), table='files'), 
            keys='id', join_type='left anti'
        )
        if newfiles.num_rows and (schematypes := init.columns_types()):
            for zipfile in newfiles.select([0]).to_pydict().get('filename'):
                if 'tripdata' in (datafile := zipfile.replace('zip','csv')):
                    if (
                        data := load.dataset(
                            datafile, types=arrow.schema(schematypes), typefile='csv', 
                            fs=filesystem('zip', fo=f'{url}{zipfile}')
                        )
                    ):
                        postgresql.adbc(
                            data=data, schema=schema, table='gte_2020', return_id=False
                        )
        return postgresql.adbc(data=newfiles, schema=schema, table='files')

    @notific.exception
    @staticmethod
    def run():
        if postgresql.setconfig((widgEx := load.widgex())):
            load.info(widgEx)
            init.dataload()

if __name__ == '__main__':
    init.run()