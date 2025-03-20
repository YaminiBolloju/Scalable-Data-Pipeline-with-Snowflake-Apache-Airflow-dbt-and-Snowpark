import os
from datetime import datetime
from airflow import DAG
from airflow.providers.dbt.cloud.operators.dbt import DbtRunOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtSeedOperator
from airflow.utils.dates import days_ago

# Define Airflow connections (use your Airflow UI to set the Snowflake connection)
# In case you are using a Snowflake connection, make sure the connection id is set in Airflow UI
snowflake_conn_id = "snowflake_conn"

# Set DBT project path
dbt_project_path = "C:/Users/bvand/OneDrive/Documents/ETLWeather/my_project/"

# Define the DAG
with DAG(
    dag_id="dbt_dag",
    schedule_interval="@daily",
    start_date=datetime(2023, 9, 10),
    catchup=False,
    max_active_runs=1,
    tags=["dbt"],
) as dag:

    # DBT run task to execute DBT models
    dbt_run = DbtRunOperator(
        task_id="dbt_run",
        dbt_bin_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt",
        models=None,  # Can specify models to run if needed, e.g., ["model1", "model2"]
        target="dev",
        profile="default",  # Or use a custom profile if needed
        project_dir=dbt_project_path,
        profiles_dir=f"{dbt_project_path}/profiles",
        conn_id=snowflake_conn_id,
    )

    # Optionally, you can use DbtSeedOperator to load data from CSV files
    dbt_seed = DbtSeedOperator(
        task_id="dbt_seed",
        dbt_bin_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt",
        target="dev",
        profile="default",  # Or use a custom profile if needed
        project_dir=dbt_project_path,
        profiles_dir=f"{dbt_project_path}/profiles",
        conn_id=snowflake_conn_id,
    )

    # Set the task dependencies
    dbt_seed >> dbt_run
