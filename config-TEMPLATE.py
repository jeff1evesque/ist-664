#!/usr/bin/python

'''

config-TEMPLATE.py, RENAME TO config.py, AND MAKE ADJUSTMENTS AS NEEDED.

'''

# general
mongos_endpoint = ['xxx.xxx.xxx.xxx:yyyy', 'xxx.xxx.xxx.xxx:yyyy']
database = 'DATABASE-NAME'
collection = 'COLLECTION-NAME'
data_directory = 'data'
username='jimmy'

# recurrent neural network
epochs = 5
batch_size = 32
split = 0.2
n_hidden = 128
post_maxlen = 10
comment_maxlen = 20
dropout = 0.2
recurrent_dropout = 0.2
checkpoint = False
checkpoint_period = 1
cwd = '~'
