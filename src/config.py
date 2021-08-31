import os
import sys

DEFAULT_STATE = 0
GTT_STOP = 1
GTT_STOP_NUMBER = 2
GTT_REPLY_NUMBER_REQ = 3
GTT_URL = 'http://www.5t.torino.it/ws2.1/rest/stops/'

DB_HOST = os.environ.get('ALFRED_DB_HOST')
DB_PORT = os.environ.get('ALFRED_DB_PORT')
DB_NAME = os.environ.get('ALFRED_DB_NAME')

ALFRED_BOT_LOG = os.environ.get('ALFRED_BOT_LOG')
TOKEN_NAME = 'ALFRED_BOT_TOKEN' if not list(sys.argv).__contains__("-dev") else 'ALFRED_BOT_DEV'
print(TOKEN_NAME)
print(os.environ)
print(os.environ.get(TOKEN_NAME))
TOKEN = os.environ.get(TOKEN_NAME)

