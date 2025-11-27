from airflow import DAG
from airflow.operators.python import PythonOperator


from common.initialize import load
from datetime import datetime
from flows.divvy_bikes.python.flowconf import flowconf
from flows.divvy_bikes.python.processing import processing


with DAG(
    dag_id="divvy_bikes",
    default_args={
        "owner": "lipebol", 
        "depends_on_past": True, 
        "start_date": datetime.now()
    },
    catchup=False, description=""
):
    
    task_1=PythonOperator(
        task_id="Requirements...",
        python_callable=load().state
    )

    task_2=PythonOperator(
        task_id="GettingData...",
        python_callable=flowconf.pull
    )

    task_3=PythonOperator(
        task_id="Processing...",
        python_callable=processing.unpack
    )

    task_4=PythonOperator(
        task_id="LoadingTripData2020...",
        python_callable=processing.tripdata_gte_2020
    )


task_1 >> task_2 >> task_3 >> task_4