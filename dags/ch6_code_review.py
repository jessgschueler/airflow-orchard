import time
import random
import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.decorators import dag, task

APPLES = ["pink lady", "jazz", "orange pippin", "granny smith", "red delicious", "gala", "honeycrisp", "mcintosh", "fuji"]

def print_hello():
    path = os.path.abspath(__file__)
    dir_name = os.path.dirname(path)
    with open(f"{dir_name}/ch6_code_review.txt", 'r') as txt:
        print(f'Hello, {txt.read()}!')

def pick_apple():
    print(random.choice(APPLES))

default_args = {
    'schedule_interval':'@once',
    'start_date': datetime.utcnow(),
    'catchup': False
} 

with DAG(
    'apple_picking',
    description='An example DAG that print user name, three randomly selected apples.',
    default_args=default_args
) as dag:

    echo_to_file=BashOperator(
        task_id='echo_to_file',
        bash_command='echo Alma > /opt/airflow/dags/ch6_code_review.txt'
    )
    print_hello = PythonOperator(
        task_id='print_hello',
        python_callable=print_hello
    )
    now_picking=BashOperator(
        task_id='now_picking',
        bash_command='echo Picking three random apples...'
    )
    apple_tasks = []
    for i in range(1,4):
        task= PythonOperator(
        task_id=f'apple_{i}',
        python_callable=pick_apple,
    )
        apple_tasks.append(task)
    
    all_done = EmptyOperator(task_id='all_done')

    echo_to_file >> print_hello >> now_picking >> apple_tasks >> all_done

