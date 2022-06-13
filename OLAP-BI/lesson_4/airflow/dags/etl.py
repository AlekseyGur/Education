from datetime import datetime
from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator


DEFAULT_ARGS = {
    "owner": "airflow",
    "start_date": datetime(2022, 6, 12),
    "retries": 1,
    "email_on_failure": False,
    "email_on_retry": False,
    "depends_on_past": False,
    'mysql_conn_id': 'mysql_stg_ods',
}

with DAG(
    dag_id="move_data_to_ods",
    default_args=DEFAULT_ARGS,
    schedule_interval="@daily",
    tags=['data-flow'],
) as dag:
   stg_drop_create = MySqlOperator(
      task_id='stg_drop_create',
      sql="sql/1-stg.sql"
   )
   
   ods_insert_new = MySqlOperator(
      task_id='ods_insert_new',
      sql="sql/2-ods.sql"
   )

   stg_drop_create >> ods_insert_new
