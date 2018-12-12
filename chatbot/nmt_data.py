#!/usr/bin/python

'''

nmt_data.py, create flatfiles for train + test.

'''

import os
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
    data = doc['value']
    if data:
        # collapse by 'link_id'
        for k, v in data.items():
            if k in combined.keys():
                combined[k] += v
            else:
                combined[k] = v

#
# train + test: comments, posts, score should be
#     the same dimension.
#
idx = int(len(combined['comments']) * 0.9)

# create nmt required input files
if not os.path.exists(directory):
    os.makedirs(directory)

    with open('analysis/test.from', 'a+') as f:
        for content in combined['posts'][idx:]:
            f.write(content+'\n')

    with open('analysis/test.to', 'a+') as f:
        for content in combined['comments'][idx:]:
            f.write(content+'\n')

    with open('analysis/train.from', 'a+') as f:
        for content in combined['posts'][:idx]:
            f.write(content+'\n')

    with open('analysis/train.to', 'a+') as f:
        for content in combined['comments'][:idx]:
            f.write(content+'\n')
