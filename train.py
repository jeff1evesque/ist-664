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

# local variables
combined = {}

# create single client
client = MongoClient(mongos_endpoint)

# combine sequence pairs
results = select(client, database, collection)
for doc in results.find():
    if doc['value']:
        for k, v in doc['value'].items():
            if k in combined.keys():
                combined[k] += v
            else:
                combined[k] = v

print(combined)

