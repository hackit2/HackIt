import os


DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
THREADS_PER_PAGE = 2

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'top secret key goes here'
SECRET_KEY = 'another top secret key goes here'

CACHE_TYPE = 'simple'

AGENT_COUNT = 40
PERCENT_UTILIZATION = 75
