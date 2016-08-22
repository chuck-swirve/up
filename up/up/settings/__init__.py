import os

IN_PROD = os.environ.get('IN_PROD', True) != 'False'

from .base import *

if IN_PROD:
    from .prod_settings import *
else:
    from .dev_settings import *
