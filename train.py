#!/usr/bin/python

'''

train.py, train a given model.

'''

from app.select import select
from app.to_from import to_from
from config import (
    mongos_endpoint,
    mongos_port,
    database,
    collection
)


# query data
data = select(
    mongos_endpoint,
    mongos_port,
    database,
    collection
)

# create sequence pairs
pairs = to_from(data)