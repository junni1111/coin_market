import pymongo
from pymongo.mongo_client import MongoClient
import datetime

cluster = MongoClient(
    "mongodb+srv://wkszlf98:1234@cluster0.rbumgu1.mongodb.net/?retryWrites=true&w=majority")
db = cluster["coin_market"]


def insert(table, data, key, value):
    collection = db[table]
    if table != "price" and table != 'post':
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


def deletePost(seller, price, coin):
    tmp = {'seller': seller, 'price': price, 'coin': coin}
    collection = db['post']

    return collection.delete_one(tmp)


def findPrice():
    collection = db["price"]
    temp = []
    for x in collection.find(sort=[('_id', pymongo.DESCENDING)]):
        temp.append(x)

    print(temp[0])
    return collection.find_one(sort=[('_id', pymongo.DESCENDING)])['price']


def findPrices():
    collection = db["price"]
    temp = []
    for x in collection.find(sort=[('_id', pymongo.DESCENDING)]):
        temp.append(x)

    return temp


def findPost(seller, price, coin):
    tmp = {'seller': seller, 'price': price, 'coin': coin}
    collection = db['post']

    return collection.find_one(tmp)


def findPosts():
    collection = db["post"]
    temp = []
    for x in collection.find(sort=[('_id', pymongo.DESCENDING)]):
        temp.append(x)

    return temp


def find(table, key, value):
    collection = db[table]
    temp = collection.find_one({key: value})
    if temp:
        return {'exist': True, 'data': temp}
    else:
        return {'exist': False}
