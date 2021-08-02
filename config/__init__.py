import os
import sys
import config.settings

# create settings object corresponding to specified env
APP_ENV = os.environ.get('APP_ENV', 'Dev')
# gets all clas attributes from the relevant <ENVIRONMENT>Config class
_current = getattr(sys.modules['config.settings'], '{0}Config'.format(APP_ENV))()

# copy attributes to the module for convenience
for atr in [f for f in dir(_current) if not '__' in f]:
   # environment can override anything
   val = os.environ.get(atr, getattr(_current, atr)) # if it can't find the var in the environemnt, overwrite with the config variables
   # add to the config module's variables
   setattr(sys.modules[__name__], atr, val)


def as_dict():
   """Return this module's set of variables as a dictionary"""
   res = {}
   for atr in [f for f in dir(config) if not '__' in f]:
       val = getattr(config, atr)
       res[atr] = val
   return res