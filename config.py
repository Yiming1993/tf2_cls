#coding = 'utf-8'
from pymongo import MongoClient
import os

def origin_path():

    origin_path = os.path.dirname(os.path.abspath(__file__))
    # print(origin_path)

    return origin_path

def db_path(db_name):
    host = '127.0.0.1'
    port = '27017'
    db_name = db_name
    uri = "mongodb://" + host + ":" + port + "/" + db_name
    client = MongoClient(uri, connect = True)
    db = client[db_name]


    # print(origin_path)

    return db