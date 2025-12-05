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
        newfiles = init.to_table(
            httpEx.scrape(
                url=(url := load.variable('DIVVYBIKES')), type='xml', tag='Contents'
            )
        ).join(
            postgresql.select(
                (schema := load.schemadb()), table= (table := 'divvybikes_files')
            ), keys='id', join_type='left anti'
        )
        if newfiles.num_rows:
            if (zip_files:= load.zip_files(with_path=False)):
                zip_files = newfiles.select([0]).join(
                    arrow.Table.from_pydict({'filename': arrow.array(zip_files)}), 
                    keys='filename', join_type='left anti'
                )
            if (zip_files := zip_files.to_pydict().get('filename')):
                for zip_file in zip_files:
                    httpEx.save(
                        savein=load.dirdownloads(), url=''.join((url,zip_file))
                    )
        return postgresql.adbc(data=newfiles, schema=schema, table=table)

    @staticmethod
    def unpack(zip_files: object):
        if not zip_files or (
            zip_files and not (
                zip_files := zip_files.select([1]).to_pydict()['filename']
            )
        ):
            zip_files = load.zip_files()
        if zip_files:
            for zip_file in zip_files:
                zip_file = load.path(
                    load.dirdownloads(), join=zip_file
                )  if not load.path(zip_file).exists() else load.path(zip_file)
                load.unzip(zip_file, suffix='.csv')
            if len((csv_files := load.csv_files())) < len(zip_files):
                raise Exception('')
            load.info(f"{len(csv_files)} files extracted.")
            return csv_files

    @staticmethod
    def gte_2020(files: list):
        if files and (
            columns := postgresql.columns(
                (schema := load.schemadb()), table= (table := 'divvybikes_gte_2020')
            )
        ):
            columnstypes = dict(
                (col, arrow.string()) if col not in ('started_at','ended_at') 
                else (col, arrow.timestamp('ms')) for col in columns
            )
            for csv_file in sorted(
                [
                    csv_file for csv_file in files if 'tripdata' in csv_file or 
                    load.path(csv_file).name == 'Divvy_Trips_2020_Q1.csv'
                ]
            ):
                if postgresql.sizedb('400 MB') and (
                    data := load.readcsv(csv_file, columns, columnstypes, sep=',')
                ):
                    postgresql.adbc(
                        data=data, schema=schema, table=table, return_id=False
                    )
        raise Exception('')
        
    @add.exception
    @staticmethod
    def run():
        if postgresql.setconfig((widgEx := load.widgex())):
            load.info(widgEx)
            if (datafiles := init.unpack(init.pull())):
                init.gte_2020(datafiles)

if __name__ == '__main__':
    init.run()