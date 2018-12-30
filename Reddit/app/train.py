#!/usr/bin/python

'''

train.py, train LSTM model

'''

import nltk
import collections
import numpy as np
from os import path
from joblib import dump
from os import path, makedirs
from keras import callbacks
from keras.layers import Input, Dense, Dropout, Activation
from keras.models import Model, save_model
from keras.layers.recurrent import LSTM
from keras.layers.wrappers import Bidirectional
from keras.layers import RepeatVector, TimeDistributed, ActivityRegularization


def train(
    posts,
    comments,
    epochs=1,
    batch_size=32,
    split=0.2,
    n_hidden=128,
    post_maxlen=10,
    comment_maxlen=20,
    dropout=0.2,
    recurrent_dropout=0.2,
    checkpoint=False,
    checkpoint_period=1,
    cwd='~'
):
    '''
    
    generate lstm recurrent neural network.    
    
    '''

    # local variables
    counter = collections.Counter()

    # create vocabulary
    sentences = posts + comments
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence):
            counter[word] += 1

    # create word + index references
    word2idx = {w:(i+1) for i,(w,_) in enumerate(counter.most_common())}
    idx2word = {v:k for k,v in word2idx.items()}
    idx2word[0] = 'PAD'
    vocab_size = len(word2idx) + 1
    print('vocabulary size: {vocab}'.format(vocab=vocab_size))

    # vectorize posts + comments
    posts_train = create_posts(posts, vocab_size, post_maxlen, word2idx)
    comments_train = create_comments(
        comments,
        vocab_size,
        comment_maxlen,
        word2idx
    )

    # recurrent neural network (LSTM)
    post_layer = Input(shape=(post_maxlen, vocab_size))
    encoder_rnn = LSTM(
        n_hidden,
        dropout=dropout,
        recurrent_dropout=recurrent_dropout
    )(post_layer)

    #
    # repeat vector: repeats the given vector iteratively for each timestep by
    #     generating it's own hidden state.
    #
    repeat_encode = RepeatVector(comment_maxlen)(encoder_rnn)

    #
    # time distributed network: allows for one-to-many (input-to-output), or
    #     many-to-many (input-to-output) cases. Specifically, the dense
    #     function is applied to each output over time. Otherwise, the dense
    #     function is only applied to the last output.
    #
    dense_layer = TimeDistributed(Dense(vocab_size))(repeat_encode)

    #
    # activation regularization (l2): penalizes for large weights, by adding
    #     value to the loss. This causes a decrease in parameter values.     
    #
    regularized_layer = ActivityRegularization(l2=1)(dense_layer)

    #
    # softmax (final layer): takes an un-normalized vector, and normalizes the
    #     the vector into a probability distribution.
    #
    softmax_layer = Activation('softmax')(regularized_layer)

    # general model
    model = Model([post_layer], [softmax_layer])
    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )
    print(model.summary())

    # directory dependency
    if not path.exists('{base}/Reddit/model'.format(base=cwd)):
        makedirs('{base}/Reddit/model'.format(base=cwd))

    # model checkpoint
    checkpoint_path = '{base}/Reddit/model/checkpoint.ckpt'.format(base=cwd)
    checkpoint_dir = path.dirname(checkpoint_path)
    cp_callback = callbacks.ModelCheckpoint(
        checkpoint_path,
        verbose=1,
        period=checkpoint_period
    )

    # train model
    posts_train_2 = posts_train.astype('float32')
    comments_train_2 = comments_train.astype('float32')
    model.fit(
        posts_train_2,
        comments_train_2,
        batch_size=batch_size,
        epochs=epochs,
        validation_split=split,
        callbacks=[cp_callback]
    )

    # idx2word: needed by separate prediction
    dump(
        idx2word,
        '{base}/Reddit/model/idx2word.pkl'.format(base=cwd),
        compress=True
    )

    # word2idx: needed by separate prediction
    dump(
        word2idx,
        '{base}/Reddit/model/word2idx.pkl'.format(base=cwd),
        compress=True
    )

    # save model
    save_model(
        model,
        '{base}/Reddit/model/rnn_lstm.h5'.format(base=cwd),
        overwrite=True,
        include_optimizer=True
    )

def encode(sentence, maxlen, vocab_size, word2idx):
    '''

    convert words to indices

    '''

    indices = np.zeros((maxlen, vocab_size))
    for i, w in enumerate(nltk.word_tokenize(sentence)):
        if i == maxlen: break

        if w in word2idx:
            indices[i, word2idx[w]] = 1
    return indices

def create_posts(posts, vocab_size, post_maxlen, word2idx):
    '''

    vectorize posts using maximum post length.

    '''

    post_idx = np.zeros(shape=(len(posts), post_maxlen, vocab_size))
    for p in range(len(posts)):
        post = encode(posts[p], post_maxlen, vocab_size, word2idx)
        post_idx[p] = post
    return post_idx

def create_comments(comments, vocab_size, comment_maxlen, word2idx):
    '''

    vectorize posts using maximum comment length.

    '''

    comment_idx = np.zeros(shape=(len(comments), comment_maxlen, vocab_size))
    for c in range(len(comments)):
        comment = encode(comments[c], comment_maxlen, vocab_size, word2idx)
        comment_idx[c] = comment
    return comment_idx
