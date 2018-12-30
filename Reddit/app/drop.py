#!/usr/bin/python

'''

upload.py, upload specified data to mongodb endpoint.

'''

import json
from os import listdir
from os.path import isfile, join


def drop_collection(client, database, collection):
    '''

    drop a specified collection.

    '''

    db = client[database]
    db.drop_collection(collection)
