from datetime import datetime, timedelta
from airflow import DAG
# from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.bash_operator import BashOperator

DEFAULT_ARGS = {
    "owner": "airflow",
    "start_date": datetime(2022, 5, 19),
    "retries": 1,
    "email_on_failure": False,
    "email_on_retry": False,
    "depends_on_past": False,
}

with DAG(
    dag_id="backup_all_db_to_vault",
    default_args=DEFAULT_ARGS,
    schedule_interval="@daily",
    tags=['data-flow'],
) as dag:
    to_vault = BashOperator(
        task_id='to_vault',
        bash_command='python3 ~/airflow/dags/tasks/to_vault.py',
    )
