from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from random import randint

def _choose_best_model(ti):
    # Pull accuracies from the XComs of the training model tasks
    accuracies = ti.xcom_pull(task_ids=[
        'training_model_A',
        'training_model_B',
        'training_model_C'
    ])
    if max(accuracies) > 8:
        return 'is_accurate'
    return 'is_inaccurate'

def _training_model(model):
    print(f"Training model {model}")
    return randint(1, 10)  # Simulate accuracy between 1 and 10

with DAG("my_dag",
         start_date=datetime(2023, 1, 1),
         schedule_interval='@daily',
         catchup=False) as dag:

    # Define PythonOperator tasks to train models A, B, and C
    training_model_tasks = [
        PythonOperator(
            task_id=f"training_model_{model_id}",
            python_callable=_training_model,
            op_kwargs={"model": model_id}
        ) for model_id in ['A', 'B', 'C']
    ]

    # Define the BranchPythonOperator to choose the best model
    choose_best_model = BranchPythonOperator(
        task_id="choose_best_model",
        python_callable=_choose_best_model
    )

    # Define BashOperator tasks to echo "accurate" or "inaccurate"
    accurate = BashOperator(
        task_id="is_accurate",
        bash_command="echo 'accurate'"
    )

    inaccurate = BashOperator(
        task_id="is_inaccurate",
        bash_command="echo 'inaccurate'"
    )

    # Set task dependencies
    training_model_tasks >> choose_best_model
    choose_best_model >> [accurate, inaccurate]
