from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.exceptions import AirflowSkipException
from datetime import datetime, timedelta

def func_task_1(**kwards):
    var = int(Variable.get('hw_etl'))
    if var == 2:
        return 'task_3'
    else:
        return 'task_2'

def func_task_2(i, **kwards):
    print(i)
    var = int(Variable.get('hw_etl'))
    if var not in [1, 2]:
         raise AirflowSkipException  

def func_task_4(**kwards):
    raise AirflowSkipException  # always skip

def func_task_5(**kwards):
    print('5')

def func_task_6(**kwargs):
    print('finished!')


default_args = {
    'start_date': datetime(2022, 1, 1)
}

dag = DAG(
    dag_id="hw_etl",
    default_args=default_args, 
    schedule_interval=None,
    catchup=False
)

task_1 = BranchPythonOperator(
    task_id='task_1',
    provide_context=True,
    python_callable=func_task_1,
    dag=dag)

task_2 = PythonOperator(
    task_id = "task_2",
    dag = dag,
    python_callable = func_task_2,
    op_kwargs = {'i': 'it works!'}
)

task_3 = BashOperator(
    task_id = "task_3",
    dag = dag,
    bash_command = 'echo "it also works!"',
)

task_4 = PythonOperator(
    task_id = "task_4",
    dag = dag,
    python_callable = func_task_4,
)

task_5 = PythonOperator(
    task_id = "task_5",
    dag = dag,
    trigger_rule = 'one_success',
    python_callable = func_task_5,
)

task_6 = PythonOperator(
    task_id = "task_6",
    dag = dag,
    trigger_rule = 'none_failed',
    python_callable = func_task_6,
)

task_1 >> task_2 >> task_6
task_1 >> [task_3, task_4] >> task_5 >> task_6
