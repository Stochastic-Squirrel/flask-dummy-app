from flask import Flask, send_file, request, redirect, url_for, render_template, Response
import os
import logging
import config
from api import api
from tasks.tasks import add
# from models import db


logging.basicConfig(level=logging.DEBUG,
                   format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                   datefmt='%Y-%m-%d %H:%M:%S',
                   handlers=[logging.StreamHandler()])

logger = logging.getLogger()


def create_app() -> Flask:
   logger.info(f'Starting app in {config.APP_ENV} environment')
   # Create a regular Flask app object
   app = Flask(__name__)
   app.config.from_object('config')

   # initialise API
   api.init_app(app)

   # initialize SQLAlchemy
   # db.init_app(app)

   # define hello world page

   @app.route('/') # root or the Home page
   def hello_world():
       return 'Hello, World! This is the landing page.'

   @app.route('/secret', methods = ["POST","GET"]) # root or the Home page
   def get_secret(image_type = None):
      image_type = request.args.get('image_type')
      if  image_type == '1': # can specify this in the url header i.e.: http://192.168.0.15:5000/secret?type=1
         filename = "static/hug.gif"
         code = 200
      elif image_type == '2':
         filename = 'static/cool.gif'
         code = 200

      elif image_type is None:
         filename = 'static/vanilla.gif'
         code = 200

      else:
         filename = "static/error.gif"
         code = 404


      print(f"Request argument for image_type is: {request.args.get('image_type')}")

      # https://stackoverflow.com/questions/8637153/how-to-return-images-in-flask-response
      return send_file(filename, mimetype='image/gif'), code

   # we can also do redirects
   @app.route('/public')
   def get_public():
      # place in the python function for url_for, and it will send the browser/client to the URL attached to this function
      return redirect(url_for('get_secret'))

   @app.route('/success/<name>') # by default if methods is not specified, only GET is valid
   def success(name):
      # templates folder needs to be in the root app folder
      return render_template("hello_template.html", name = name)

   @app.route('/login',methods = ['POST'])
   # the HTML file allows us to send a form POST, which means that we can use this endpoint here
   # TODO: for some reason the second form isn't posting information
   def login():
      if request.args.get("nm") != '':
         print(request.form)
         if request.method == 'POST':
            user = request.form['nm'] # name of the element
            return redirect(url_for('success', name = user))

   @app.route('/add',methods = ['POST','GET'])
   def add_numbers(): 
      x = request.args.get("x")
      y = request.args.get("y")
      result = add.delay(x,y) # this takes a long time
      return {"result": result.get()}, 200

   return app # return this Flask app


if __name__ == "__main__":
   app = create_app()
   app.run(host='0.0.0.0', debug=True)