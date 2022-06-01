from datetime import datetime, timedelta
from airflow import DAG
# from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
# from airflow.operators.bash_operator import BashOperator

import tasks.backup


DEFAULT_ARGS = {
    "owner": "airflow",
    "start_date": datetime(2022, 5, 19),
    "retries": 1,
    "email_on_failure": False,
    "email_on_retry": False,
    "depends_on_past": False,
}

with DAG(
    dag_id="backup_db_line_by_line",
    default_args=DEFAULT_ARGS,
    schedule_interval="@daily",
    tags=['data-flow'],
) as dag:
    backup_1 = PythonOperator(task_id='backup_part',
                              python_callable=backup.make,
                              op_args=('part', 'p_partkey'))

    backup_2 = PythonOperator(task_id='backup_lineitem',
                              python_callable=backup.make,
                              op_args=('lineitem', 'l_orderkey'))

    backup_3 = PythonOperator(task_id='backup_partsupp',
                              python_callable=backup.make,
                              op_args=('partsupp', 'ps_partkey'))

    backup_4 = PythonOperator(task_id='backup_region',
                              python_callable=backup.make,
                              op_args=('region', 'r_regionkey'))

    backup_5 = PythonOperator(task_id='backup_orders',
                              python_callable=backup.make,
                              op_args=('orders', 'o_orderkey'))

    backup_6 = PythonOperator(task_id='backup_supplier',
                              python_callable=backup.make,
                              op_args=('supplier', 's_suppkey'))

    backup_7 = PythonOperator(task_id='backup_customer',
                              python_callable=backup.make,
                              op_args=('customer', 'c_custkey'))

    backup_8 = PythonOperator(task_id='backup_nation',
                              python_callable=backup.make,
                              op_args=('nation', 'n_nationkey'))

    # запускаем все task'и последовательно
    backup_1 >> backup_2 >> backup_3 >> backup_4 >> \
    backup_5 >> backup_6 >> backup_7 >> backup_8

    # запускаем все task'и параллельно
    # [backup_1, backup_2, backup_3, backup_4, backup_5, backup_6, backup_7, backup_8]
