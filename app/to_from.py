#!/usr/bin/python

'''

to_from.py, split list of dicts into 'to' and 'from' lists.

'''


import pandas as pd
from itertools import repeat

def to_from(data):
    # local variables
    to_body = []
    from_body = []

    #
    # convert to dataframe: for smaller subsets, list comprehension can
    #     perform better than numpy structures. However, as subsets are
    #     increased to 1000+, the performance generally is better for
    #     numpy arrays.
    #
    df = pd.DataFrame(data)

    # split into 'to' and 'from'
    for i, row in df.iterrows():
        # attain 'id' from 'parent_id'
        id = row.parent_id.split('_',1)[1]

        # append 'to' and 'from'
        if (id == row.id and row.body != df.body):
            to_body.append(row[['body']])
            from_body.extend(repeat(row.body, len(to)))

    # return data
    return({'to': to_body, 'from': from_body})
