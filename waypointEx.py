from common.addEx import add
from common.dbEx import postgresql
from common.httpEx import httpEx
from common.loadEx import load, system
from common.mountEx import mount
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
    def pull():
        __newfiles = init.to_table(
            httpEx.scrape(
                url=(__url := load.variable('DIVVYBIKES')), 
                type='xml', tag='Contents'
            )
        ).join(
            postgresql.select(
                (schema := load.schemadb()), 
                table= (table := 'divvybikes_files')
            ), keys='id', join_type='left anti'
        )
        if __newfiles.num_rows:
            if (__files:= load.zip_files(with_path=False)):
                for filename in __newfiles.select([0]).join(
                    arrow.Table.from_pydict({'filename': arrow.array(__files)}), 
                    keys='filename', join_type='left anti'
                ).to_pydict().get('filename'):
                    httpEx.save(
                        savein=load.dirdownloads(), url=''.join((__url,filename))
                    )
        return postgresql.adbc(data=__newfiles, schema=schema, table=table)
        
    # @add.exception
    @staticmethod
    def run():
        if postgresql.setconfig((widgEx := load.widgex())):
            load.info(widgEx)
            return init.pull()

if __name__ == '__main__':
    print(init.run())