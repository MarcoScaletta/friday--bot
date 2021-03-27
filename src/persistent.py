import config
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

cred = credentials.Certificate("google-credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
collection = "favorite-stops"
document = db.collection("favorite-stops").document('users')

# from pymongo import MongoClient
# import config

# user = config.DB_USER
# password = config.DB_PASSWORD
# db_name = config.DB_NAME

# url = config.DB_HOST + ":" + config.DB_PORT + "/"+db_name

# client = MongoClient("mongodb://"+user+":"+password+"@"+url, retryWrites=False)
# db = client[db_name]

# from firebase_admin import db

def get_favorite_stop(chatID):
    return document.get().to_dict()[chatID]


def exists_chatID(chatID):
    doc = document.get().to_dict()
    print(doc)
    if chatID in doc:
        print("Exists [" + chatID +"] " + doc[chatID])
        return doc[chatID]
    return  None

def insert_chatID(chatID):
    doc = document.set({chatID:"NULL"},merge=True)
    return doc

def insert_if_not_exists(chatID):
    if not exists_chatID(chatID):
        insert_chatID(chatID)

def set_fav_stop(chatID,stop):
    return document.set({chatID:stop},merge=True)