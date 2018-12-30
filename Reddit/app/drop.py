#!/usr/bin/python

'''

drop.py, drop specified object from database.

'''


def drop_collection(client, database, collection):
    '''

    drop a specified collection.

    '''

    db = client[database]
    db.drop_collection(collection)
