# This module defines the tasks for a celery worker that you need to create. you do NOT call the functions within this file, do it in a runner

from celery import Celery
from time import sleep
app = Celery(backend = 'rpc://', broker='pyamqp://guest:guest@localhost:5672')
result_persistent = True

@app.task
def add(x, y):
    sleep(10)
    return x + y