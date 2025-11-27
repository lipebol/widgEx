from common.db import db
from common.initialize import load
from common.httpEx import httpEx
from xmltodict import parse
import pyarrow as arrow

class flowconf:

    schema = 'divvy_bikes'

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
        __url = 'https://divvy-tripdata.s3.amazonaws.com'
        __newfiles = flowconf.to_table(
            httpEx.scrape(url=__url,type='xml',tag='Contents')
        )
        if (__files := db.select(flowconf.schema, 'files')):
            __newfiles = __newfiles.join(
                flowconf.to_table(__files), 
                keys='id', join_type='left anti'
            )
        if __newfiles.num_rows:
            if (__files:= load().zip_files(with_path=False)):
                __newfiles = __newfiles.select([0]).join(
                    arrow.Table.from_pydict({'filename': arrow.array(__files)}), 
                    keys='filename', join_type='left anti'
                )
            for filename in __newfiles.to_pydict().get('filename'):
                httpEx.save(flowpath=load().flow, url=__url + filename)
        return db.adbc(__newfiles, flowconf.schema, 'files')