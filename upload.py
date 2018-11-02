#!/usr/bin/python

'''

upload.py, upload specified data to mongodb endpoint.

'''

import json
from os import listdir
from os.path import isfile, join
from pymongo import MongoClient
from config import mongos_endpoint, mongos_port, database, collection


# endpoint
client = MongoClient(mongos_endpoint:mongos_port)

# database + collection
db = client[database]
col = db[collection]

# insert data
data = []
for f in listdir('data'):
    if isfile(join('data', f):
        for line in f.readlines():
            # verify valid json
            try:
                valid = json.loads(line)
            except ValueError, e:
                valid = False
                print('Not valid json: {}'.format(e))

            # append to bulk array
            if valid:
                data.append(line)

# insert to mongodb
if data:
    post_id = mycol.insert_many(line).inserted_id
    print('post_id: {}'.format(post_id))
