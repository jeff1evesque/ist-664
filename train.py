#!/usr/bin/python

'''

train.py, train a given model.

'''

from pymongo import MongoClient
from app.select import select
from config import (
    mongos_endpoint,
    database,
    collection
)

# create single client
client = MongoClient(mongos_endpoint)

# create sequence pairs
pairs = select(client, database, collection)
for doc in pairs.find():
    print(doc)

