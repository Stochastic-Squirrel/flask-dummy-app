# Next goes the API package, which defines the REST API using the Flask-Restful package. 
# Our app is just a demo and will have only two endpoints:

# /process_data – Starts a dummy long operation on a Celery worker and returns the ID of a new task.
# /tasks/<task_id> – Returns the status of a task by task ID.

import time
from flask import jsonify
from flask_restful import Api, Resource
from flask import request
from tasks import celery
import json
import config

api = Api(prefix=config.API_PREFIX)


class TaskStatusAPI(Resource):
   def get(self, task_id):
       task = celery.AsyncResult(task_id)
       return jsonify(task.result)

class JokeAPI(Resource):
   def get(self, name: str): # for URL headline arguments
      author = request.form.get("author","Anonymous") # get data from post method, i.e. the request body

      # name here, when declared in the method signature, is passed in as a PARAMETER and NOT a request body argument
      return {'joke':f"{name}, you are the joke! Author: {author}"}, 200


class DataProcessingAPI(Resource):
   def post(self):
       task = process_data.delay()
       return {'task_id': task.id}, 200


# asynchronous task
@celery.task()
def process_data():
   print("Starting task and processing data")
   time.sleep(5)
   print("Finished task that processed data!")


# data processing endpoint
api.add_resource(DataProcessingAPI, '/process_data')
# task status endpoint
api.add_resource(TaskStatusAPI, '/tasks/<string:task_id>')
api.add_resource(JokeAPI, '/jokes/<string:name>')