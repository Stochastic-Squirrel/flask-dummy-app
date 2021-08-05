# This module defines the tasks for a celery worker that you need to create. you do NOT call the functions within this file, do it in a runner



from celery import Celery
from time import sleep
app = Celery(backend = 'rpc://', broker='pyamqp://guest:guest@localhost:5672')
result_persistent = True


app.conf.task_routes = {'tasks.tasks.*': {'queue': 'maths_queue'}}

# this will place all tasks define in this file under the name task_queue
# NOTE: when we fire up worker(s) we can tell certain workers to only look at certain queues,
# therefore if we wish to fire up a single worker to look at the queue called 'maths_queue'
#  celery -A tasks.tasks worker -l INFO -Q maths_queue 
# see more here https://docs.celeryproject.org/en/stable/userguide/routing.html
# -A == --app


@app.task
def add(x, y):
    sleep(10)
    return x + y