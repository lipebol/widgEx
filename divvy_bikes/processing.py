from .flowconf import flowconf
from common.db import db
from common.initialize import load
from common.file import file
import pyarrow as arrow


class processing:


    @staticmethod
    def unpack():
        __zip_files = load().zip_files()
        for zip_file in __zip_files:
            load.unzip(load.path(zip_file), suffix='.csv')
        if len(load().csv_files) < len(__zip_files):
            raise Exception('')
        return load.variable('MESSAGE_SUCCESS')

    @staticmethod
    def tripdata_gte_2020():
        __cols = db.columns(flowconf.schema, 'tripdata_gte_2020')
        __types = dict(
            (col,arrow.string()) if col not in ('started_at','ended_at') 
            else (col,arrow.timestamp('ms')) for col in __cols
        )
        __csv_files = sorted([
            csv_file for csv_file in load().csv_files 
            if 'tripdata' in csv_file or 
            load.path(csv_file).name == 'Divvy_Trips_2020_Q1.csv'
        ])
        for csv_file in __csv_files:
            __data = file.load_csv(csv_file, __cols, __types, sep=',')
            __todb = db.adbc(__data, flowconf.schema, 'tripdata_gte_2020')
            print(f'{load.path(csv_file).name}[{__data.num_rows} rows] ({__todb})')
        return load.variable('MESSAGE_SUCCESS')