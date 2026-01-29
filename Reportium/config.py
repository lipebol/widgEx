from common.httpEx import httpEx
from common.loadEx import load, system
from common.ui import uiall
from datetime import datetime
from os import listdir, makedirs
import pyarrow as arrow


class reportium:
    
    uiall.name('Reportium')

    @staticmethod
    def dir():
        if (
            default := load.path(load.path(user=True), join='.reportium')
        ) and (assets := load.path(default, join='assets')):
            if not load.checkpath(default):
                for dir in [default, assets]:
                    makedirs(dir)
            if not listdir(assets):
                for env in [
                    'REPORTIUM_LOGO', 
                    'REPORTIUM_LINUX_ICON', 
                    'REPORTIUM_WINDOWS_ICON'
                ]:
                    httpEx.save(url=load.variable(env), savein=assets)
            return default

    @staticmethod
    def assets():
        if (assetsdir := load.path(reportium.dir(), join='assets')):
            if (
                icon := ''.join(
                    img for img in listdir(assetsdir) 
                    if system._os().lower() in img
                )
            ):
                for asset in [icon, 'reportium.png']:
                    yield load.path(assetsdir, join=asset)

    @staticmethod
    def between(**kwargs) -> dict:
        return {
            'between': '|'.join(
                [
                    str(datetime.strptime(date,'%d/%m/%Y').date()) 
                    for date in kwargs.values() if date != ''
                ]
            )
        }

    @staticmethod
    def query(**kwargs):
        return load.string(
            kwargs, template="""
            query {
                DivvyBikes(by: "started_at", between: "$between", info: $info) {
                    ...on DivvyBikes {
                        data {
                            ride_id
                            rideable_type
                            started_at
                            ended_at
                            start_station_name
                            start_station_id
                            end_station_name
                            end_station_id
                            start_lat
                            start_lng
                            end_lat
                            end_lng
                            member_casual
                        }
                    }

                    ...on Info {
                        total
                        pages
                        columns
                    }

                    ...on Errors {
                        error
                        message
                        status_code
                    }
                }
            }
            """
        )

    @staticmethod
    def request(**kwargs):
        return httpEx.graphql(
            url='http://localhost/api/v2/graphql', 
            query=reportium.query(**kwargs)
        )

    @staticmethod
    def info(dates: dict) -> bool:
        if (
            info := reportium.request(
                **{**reportium.between(**dates), 'info': 'true'}
            )
        ):
            infowindow = uiall.generic(
                message=info.get('message'), 
                sizes=[0.3088235294117647, 0.20833333333333334] 
            ) if 'error' in info.keys() else uiall.generic(
                button='Continuar', message=load.string(
                    info, template=load.variable('REPORTIUM_INFO_TEXT')
                ), sizes=[0.4117647058823529, 0.2604166666666667] 
            )

            if infowindow:
                return info
    
    @staticmethod
    def data(dates: dict, info: dict) -> list or dict:
        choosewindow, savein = uiall.choose(assets=reportium.assets())
        params = reportium.between(**dates)
        with arrow.csv.CSVWriter(
            (
                filename := load.string(
                    {'savein': savein, 'now': params.get('between')}, 
                    template=load.variable('REPORTIUM_FILE')
                )
            ), schema=arrow.schema(
                [
                    arrow.field(column, arrow.string()) 
                    for column in info.get('columns')
                ]
            ), write_options=arrow.csv.WriteOptions(delimiter=';')
        ) as csvwriter:
            for page in range(int(info.get('pages'))):
                data = arrow.RecordBatch.from_pylist(
                    reportium.request(
                        **{**params, 'info': f'false, page: {page+1}'}
                    ).get('data')
                )
                csvwriter.write(data)
                load.info(f'Writted {data.num_rows} rows in "{filename}".')
        choosewindow.Hide()
        uiall.generic(
            message='Concluído com Sucesso!',
            sizes=[0.3088235294117647, 0.20833333333333334]
        )


    