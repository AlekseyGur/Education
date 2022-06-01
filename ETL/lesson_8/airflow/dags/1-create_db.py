from datetime import datetime, timedelta
from airflow import DAG
# from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
# from airflow.operators.bash_operator import BashOperator


DEFAULT_ARGS = {
    "owner": "airflow",
    "start_date": datetime(2022, 5, 30),
    "retries": 1,
    "email_on_failure": False,
    "email_on_retry": False,
    "depends_on_past": False,
}

with DAG(
    dag_id="1-create_db",
    default_args=DEFAULT_ARGS,
    schedule_interval="@once",
    tags=['data-flow'],
) as dag:
    create_tables_step = PostgresOperator(
        task_id="1-create_db",
        postgres_conn_id="postgres_to",
        sql="sql/1-create_db.sql"
    )
