#!/usr/bin/python

'''

train.py, train a given model.

'''

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
    mongos_port,
    database,
    collection
)

# create sequence pairs
pairs = select(client)
for doc in pairs.find():
    print(doc)

