
from pymongo import MongoClient
import config

user = config.DB_USER
password = config.DB_PASSWORD
db_name = config.DB_NAME

url = config.DB_HOST + ":" + config.DB_PORT + "/"+db_name

client = MongoClient("mongodb://"+user+":"+password+"@"+url, retryWrites=False)
db = client[db_name]


def exists_chatID(chatID):
    obj = db.chatID.find_one({"chatID": chatID})
    print(obj)
    return obj is not None


def insert_chatID(chatID):
    obj = db.chatID.insert_one({"chatID": chatID})
    return obj


def insert_if_not_exists(chatID):
    if not exists_chatID(chatID):
        return insert_chatID(chatID)
    return None
