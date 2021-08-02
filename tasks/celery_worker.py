# This module is required to start and initialize a Celery worker, 
# which will run in a separate Docker container. It initializes the Flask application context 
# to have access to the same environment as the application. If that’s not required, these lines can be safely removed.


from app import create_app # user created module

app = create_app()
app.app_context().push()

from tasks import celery
