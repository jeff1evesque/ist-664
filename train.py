#!/usr/bin/python

'''

train.py, train a given model.

'''

from pymongo import MongoClient
from app.select import select
from config import (
    mongos_endpoint,
    mongos_port,
    database,
    collection
)

# create single client
client = MongoClient('{}:{}'.format(
    mongos_endpoint,
    mongos_port
))

# create sequence pairs
pairs = select(client, database, collection)
for doc in pairs.find():
    print(doc)

