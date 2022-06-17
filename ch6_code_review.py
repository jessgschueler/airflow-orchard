import time
import random
import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator, BashOperator
from airflow.decorators import dag, task

python APPLES = ["pink lady", "jazz", "orange pippin", "granny smith", "red delicious", "gala", "honeycrisp", "mcintosh", "fuji"]

@task
def print_hello():
    path = os.path.abspath(__file__)
    dir_name = os.path.dirname(path)
    with open(f"{dir_name}/hello.txt", 'r') as txt:
        print(txt)



@dag(
    schedule_interval='@once',
    start_date=datetime.utcnow(),
    catchup=False
)    
    echo_to_file=BashOperator(
        task_id='echo_to_file',
        bash_command='echo $USER > ch6_code_review.txt'
    )
    print_hello = print_hello()

    now_picking=BashOperator(
        task_id='now_picking',
        bash_command='echo Picking three random apples...'
    )


