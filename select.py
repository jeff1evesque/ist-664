#!/usr/bin/python

'''

select.py, select specified data from mongodb endpoint.

'''


from pymongo import MongoClient
from config import (
    mongos_endpoint,
    mongos_port,
    database,
    collection
)

def select():
    # endpoint
    client = MongoClient('{}:{}'.format(
        mongos_endpoint,
        mongos_port
    ))

    # database + collection
    db = client[database]
    col = db[collection]

    # select data
    data = []
    cursor = col.find({})
    for document in cursor:
        data.append(document)

    # return data
    return(data)
