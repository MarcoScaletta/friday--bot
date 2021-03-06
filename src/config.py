import os 

DEFAULT_STATE = 0
GTT_STOP = 1
GTT_STOP_NUMBER = 2
GTT_URL = 'http://www.5t.torino.it/ws2.1/rest/stops/'

DB_HOST = os.environ.get('ALFRED_DB_HOST')
DB_PORT = os.environ.get('ALFRED_DB_PORT')
DB_NAME = os.environ.get('ALFRED_DB_NAME')

ALFRED_BOT_LOG = os.environ.get('ALFRED_BOT_LOG')
TOKEN = os.environ.get('ALFRED_BOT_TOKEN')

DB_USER = os.environ.get('ALFRED_DB_USER')
DB_PASSWORD = os.environ.get('ALFRED_DB_PASSWORD')
