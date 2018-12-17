#!/usr/bin/python

'''

upload.py, upload specified data to mongodb endpoint.

'''

import json
from os import listdir
from os.path import isfile, join


def insert(client, db, col, data_directory='data'):
    # insert data
    data = []
    for f in listdir(data_directory):
        file = join(data_directory, f)
        if isfile(file):
            with open(file) as fp:
                for line in fp.readlines():
                    # verify valid json
                    try:
                        valid = json.loads(line)
                        data.append(valid)
                        print('insert: {}'.format(line))
                    except ValueError as e:
                        valid = False
                        print('Not valid json: {}'.format(e))

    # insert to mongodb
    if data:
        post_id = col.insert_many(data).inserted_ids
        print('post_id: {}'.format(post_id))
