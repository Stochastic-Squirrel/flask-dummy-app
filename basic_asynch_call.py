# -*- coding: utf-8 -*-
# need to make sure that
# 1) A message broker is running, i.e. rabbitmq in its container and expose the correct ports
## docker run -d --hostname my-rabbit -p 8080:15672 -p 5672:5672 rabbitmq:3-management
# 2.) You have fired up the celery worker on your end and that you tell it where the .py files are for your tasks
## celery -A tasks.tasks worker -l INFO   (in module tasks within tasks.py)
from tasks.tasks import *
from tasks.tasks import add
result = add.delay(4, 4)
print(result)
print(result.ready())
# this will be false as this is working in the background
print("This is something completely different that i am doing whilst the asynch task is running!")
print(f"Here is the result: {result.get()}")

