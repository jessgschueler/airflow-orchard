from operator import truediv
from pickle import TRUE
import time
import random
import os
from datetime import datetime
from airflow import DAG
from airflow.decorators import dag, task

#create our tasks
@task
def rain():
    """
    returns a random amount of rain
    """
    return random.randint(1,5)

@task
def roots(water):
    """
    accepts return of rain and returns either 3 or 1
    """
    if int(water) > 3:
        return 3
    else:
        return 1

@task
def trunk(grow_int):
    """
    accepts return of roots and returns a random amount of nutrients
    """
    if grow_int >= 3:
        nutrients = random.randint(1,10)
        return nutrients
    else:
        return 0

@task
def branch(nutr_int):
    """
    accepts return of nutrients and prints either 'Apples' or 'Better luck next year!'
    """
    if nutr_int > 3:
        print('Apples!')
    else:
        print('Better luck next year!')

#set dag attributes
@dag(
    schedule_interval='@once',
    start_date=datetime.utcnow(),
    catchup=False,
)
#function that calls all of our tasks to create dag
def apple_tree():
    #create rain task
    rain_task = rain()
    #use for loop to generate three root tasks
    root_tasks = []
    for i in range(1,4):
        root = roots(rain_task)
        root_tasks.append(root)
    #use a random choice of output from the root tasks for the input of trunk task
    trunk_task = trunk(random.choice(root_tasks))
    #use for loop to generate 5 branch tasks
    branch_tasks = []
    for i in range(1,5):
        branch_task = branch(trunk_task)
        branch_tasks.append(branch_task)
    #establish task order   
    rain_task >> root_tasks >> trunk_task >> branch_tasks
#create dag
apple_tree = apple_tree()



