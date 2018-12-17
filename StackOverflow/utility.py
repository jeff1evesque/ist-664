#!/usr/bin/python

'''

utility.py, helper functions.

'''


from nltk.tokenize import TreebankWordTokenizer, RegexpTokenizer
import joblib

def tokenize(doc):
    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
    doc = ' '.join(RegexpTokenizer(pattern=r'\b[^\d\W^_]+\b').tokenize(doc))
    doc = TreebankWordTokenizer().tokenize(doc)
    doc = [term for term in doc if term not in punctuation]
    doc = [term for term in doc if len(term) > 2]
    return doc

def so_model(cwd):
    '''

    return unserialized model.

    '''

    return joblib.load('{base}/StackOverflow/SO_RF_Model_new.pkl'.format(base=cwd))
