# The tasks package contains Celery initialization code. Config package, which will already 
# have all settings copied on module level upon initialization, 
# is used to update Celery configuration object in 
# case we will have some Celery-specific settings in the future—for example,
#  scheduled tasks and worker timeouts.


from celery import Celery
import config


def make_celery():
   celery = Celery(__name__, broker=config.CELERY_BROKER)
   celery.conf.update(config.as_dict()) # celery needs all the environment variables as a dictionary
   return celery


celery = make_celery()