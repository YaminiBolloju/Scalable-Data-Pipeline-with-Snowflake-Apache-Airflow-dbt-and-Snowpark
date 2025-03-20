import os
from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

# DBT project configuration
DBT_PROJECT_PATH = "C:/Users/bvand/OneDrive/Documents/ETLWeather/my_project/"
DBT_VENV_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"
POSTGRES_CONN_ID = 'postgres_default'

# Default arguments
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

# Create the DBT DAG
with DAG(
    dag_id="dbt_dag",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    def run_dbt():
        """Run DBT using PythonOperator."""
        os.system(f"{DBT_VENV_PATH} run --project-dir {DBT_PROJECT_PATH}")

    # Python operator to run DBT
    run_dbt_task = PythonOperator(
        task_id="run_dbt_task",
        python_callable=run_dbt,
    )

    run_dbt_task
