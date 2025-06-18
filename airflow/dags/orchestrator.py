import sys
sys.path.append('/opt/airflow')
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from weather_api_pull.app import main

load_dotenv('/app/.env')

default_args = {
    'start_date': datetime(2025, 6, 15),
    'description': 'A simple weather data pipeline',
    'catchup': False,
}


with DAG(
    'weather_api_dbt_orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=5),  # Run every 5 minutes
    max_active_runs=1,  # Only 1 DAG run at a time
    max_active_tasks=1,  # Only 3 tasks from this DAG can run at once
) as dag:
    
    start = EmptyOperator(task_id='start')

    insert_data = PythonOperator(
        task_id='insert_weather_data',
        python_callable=main,
        op_args=['london'],  # You can change 'london' to any city you want to fetch data for
    )
    
    dbt_data = DockerOperator(
        task_id='transform_weather_data',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.0',
        command='run',
        working_dir='/usr/app/',
        mounts=[
            Mount(
                source='/Users/ragoyal/Desktop/ATOM-Files/weather-dashboard/dbt/dbt_project',
                target='/usr/app/',
                type='bind'
            ),
            Mount(
                source='/Users/ragoyal/Desktop/ATOM-Files/weather-dashboard/dbt/profiles.yml',
                target='/root/.dbt/profiles.yml',
                type='bind'
            ),
            Mount(
                source='/Users/ragoyal/Desktop/ATOM-Files/weather-dashboard/.env',
                target='/usr/app/.env',
                type='bind'
            ),
        ],
        environment={
            'POSTGRES_DB': os.environ.get('POSTGRES_DB'),
            # Add other required env vars if needed
        },
        network_mode='weather-dashboard_my_network',
        auto_remove='success',
        docker_url='unix://var/run/docker.sock',
        tty=True
    )

    end = EmptyOperator(task_id='end')
    
    start >> insert_data >> dbt_data >> end