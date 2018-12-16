#!/usr/bin/python

'''

utility.py, helper function.

'''

import numpy as np
import pandas as pd
from nltk import word_tokenize, tag


def penn_scale():
    '''

    categorization of penn-tree
    
        - https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

    '''

    return {
        'CC': 1,
        'CD': 2,
        'DT': 3, 
        'EX': 4,
        'FW': 5,
        'IN': 6,
        'JJ': 7,
        'JJR': 8,
        'JJS': 9,
        'LS': 10,
        'MD': 11,
        'NN': 12,
        'NNS': 13,
        'NNP': 14,
        'NNPS': 15,
        'PDT': 16,
        'POS': 17,
        'PRP': 18,
        'PRP$': 19,
        'RB': 20,
        'RBR': 21,
        'RBS': 22,
        'RP': 23,
        'SYM': 24,
        'TO': 25,
        'UH': 26,
        'VB': 27,
        'VBD': 28,
        'VBG': 29,
        'VBN': 30,
        'VBP': 31,
        'VBZ': 32,
        'WDT': 33,
        'WP': 34,
        'WP$': 35,
        'WRB': 36
    }

def normalize_data(X_data, stop_gap=40, stop_value=0, train=False):
    '''

    Ensure each sentence has exactly 'stop_gap' number of columns.

    '''

    if train:
        ## ensure nested lists same length
        length = len(sorted(X_data, key=len, reverse=True)[0])
        X_data=np.array([xi+[stop_gap]*(length-len(xi)) for xi in X_data])
        X_data=pd.DataFrame(X_data)

        ## get shape of dataframe
        rows_train, columns_train = X_data.shape
        delta = stop_gap - columns_train

        ##
        ## columns fixed to 40:
        ##
        ## https://github.com/jeff1evesque/ist-664/issues/62#issuecomment-447223456
        ##
        if delta > 0 and delta <= stop_gap:
            for i in range(delta):
                X_data['filler-{}'.format(i)] = stop_value

        if delta < 0:
            rem_list = [x for x in range(abs(columns_train))][:delta]
            X_data = X_data.iloc[:,rem_list]

    else:
        columns_train = len(X_data)
        delta = stop_gap - columns_train

        ##
        ## columns fixed to 40:
        ##
        ## https://github.com/jeff1evesque/ist-664/issues/62#issuecomment-447223456
        ##
        if delta > 0 and delta <= stop_gap:
            for i in range(delta):
                X_data.append(stop_value)

        if delta < 0:
            rem_list = [x for x in range(abs(columns_train))][:delta]
            X_data = X_data[:len(X_data) - rem_list]

    ## return train + test
    return(X_data)

def tokenizer(sentence):
    '''

    tokenize + parts of speech

    '''

    pos_scale = penn_scale()
    pos_scale = penn_scale()
    sent = word_tokenize(sentence)
    pos = tag.pos_tag(sent)
    return([x[1] for x in pos if x[1] and x[1] in pos_scale])

def replace(list, dictionary):
    '''

    replace list item with corresponding dict value

    '''

    return [dictionary.get(item, item) for item in list]
