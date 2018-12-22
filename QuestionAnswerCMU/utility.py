#!/usr/bin/python

'''

utility.py, helper function.

'''

import numpy as np
import pandas as pd
import joblib
from nltk import word_tokenize, tag


def penn_scale():
    '''

    categorization of penn-tree
    
        - https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

    '''

    return {
        'CC': 2,
        'CD': 3,
        'DT': 4,
        'EX': 5,
        'FW': 6,
        'IN': 7,
        'JJ': 8,
        'JJR': 9,
        'JJS': 10,
        'LS': 11,
        'MD': 12,
        'NN': 13,
        'NNS': 14,
        'NNP': 15,
        'NNPS': 16,
        'PDT': 17,
        'POS': 18,
        'PRP': 19,
        'PRP$': 20,
        'RB': 21,
        'RBR': 22,
        'RBS': 23,
        'RP': 24,
        'SYM': 25,
        'TO': 26,
        'UH': 27,
        'VB': 28,
        'VBD': 29,
        'VBG': 30,
        'VBN': 31,
        'VBP': 32,
        'VBZ': 33,
        'WDT': 34,
        'WP': 35,
        'WP$': 36,
        'WRB': 37
    }

def normalize_data(X_data, stop_gap=40, stop_value=1, train=False):
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
    sent = word_tokenize(sentence)
    pos = tag.pos_tag(sent)
    return([x[1] for x in pos if x[1] and x[1] in pos_scale])

def replace(list, dictionary):
    '''

    replace list item with corresponding dict value

    '''

    return [dictionary.get(item, item) for item in list]

def qa_model(cwd):
    '''

    return unserialized model.

    '''

    return joblib.load('{base}/QuestionAnswerCMU/model/random_forest.pkl'.format(base=cwd))
