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
    dag_id="backup_all_db",
    default_args=DEFAULT_ARGS,
    schedule_interval="@daily",
    tags=['data-flow'],
) as dag:
    save_old_db_to_csv = BashOperator(
        task_id='save_old_db_to_csv',
        bash_command='python3 ~/airflow/dags/tasks/save_old_db_to_csv.py',
    )

    load_csv_to_new_db = BashOperator(
        task_id='load_csv_to_new_db',
        bash_command='python3 ~/airflow/dags/tasks/load_csv_to_new_db.py',
    )

    save_old_db_to_csv >> load_csv_to_new_db
