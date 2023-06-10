import pymongo
from pymongo.mongo_client import MongoClient
import datetime

cluster = MongoClient(
    "mongodb+srv://wkszlf98:1234@cluster0.rbumgu1.mongodb.net/?retryWrites=true&w=majority")
db = cluster["coin_market"]


def insert(table, data, key, value):
    collection = db[table]
    temp = collection.find_one({key: value})
    if temp:
        return {'exist': True, 'data': temp}

    if table == 'user':
        data['coin'] = 0
        data['money'] = 0
    collection.insert_one(data)
    return {'exist': False, 'data': collection.find_one(data)}


def update(table, key, value, data):
    collection = db[table]
    myquery = {key: value}
    newvalues = {"$set": data}
    collection.update_one(myquery, newvalues)

    temp = collection.find_one({key: value})
    return temp


def delete(table, key, value):
    collection = db[table]
    collection.delete_one({key: value})


def find(table, key, value):
    collection = db[table]
    temp = collection.find_one({key: value})
    if temp:
        return {'exist': True, 'data': temp}
    else:
        return {'exist': False}
