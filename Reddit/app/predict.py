#!/usr/bin/python

'''

predict.py, using loaded lstm model generate sequence.

'''

from keras.models import load_model
import numpy as np
from joblib import load
from Reddit.app.train import create_posts


def predict(post, post_maxlen, cwd=''):
    '''

    predict sequence response.

    '''

    # load model + converter
    model = load_model('{base}/Reddit/model/rnn_lstm.h5'.format(base=cwd))
    word2idx = load('{base}/Reddit/model/word2idx.pkl'.format(base=cwd))

    # vectorize post
    vocab_size = len(word2idx) + 1
    vectorized = create_posts(post, vocab_size, post_maxlen, word2idx)

    # predict reply
    comment = model.predict(vectorized)
    return(decode(comment, cwd))

def decode(posts, cwd, calc_argmax=True):
    '''

    convert indices to words.

    '''

    # local variables
    result = []

    # load indexer
    idx2word = load('{base}/Reddit/model/idx2word.pkl'.format(base=cwd))
    if calc_argmax:
        posts = np.argmax(posts, axis=-1)

    # convert index to words
    for sentence in posts:
        result.append(' '.join(idx2word[x] for x in sentence))

    return result
