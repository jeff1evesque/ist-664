#!/usr/bin/python

'''

train.py, train LSTM model

'''

import nltk
import collections
import numpy as np
from joblib import dump
from os import path, makedirs
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
    for comment in comments:
        for word in nltk.word_tokenize(comment):
            counter[word] += 1

    word2idx = {w:(i+1) for i,(w,_) in enumerate(counter.most_common())}
    idx2word = {v:k for k,v in word2idx.items()}
    idx2word[0] = 'PAD'
    vocab_size = len(word2idx) + 1
    print('vocabulary size: {vocab}'.format(vocab=vocab_size))

    # idx2word: needed by separate prediction
    if not path.exists('{base}/model'.format(base=cwd)):
        makedirs('{base}/model'.format(base=cwd))
    dump(model, '{base}/model/idx2word.pkl'.format(base=cwd), compress=True)

    posts_train = create_posts(posts, vocab_size, post_maxlen, word2idx)
    comments_train = create_comments(
        comments,
        vocab_size,
        comment_maxlen=comment_maxlen
    )

    # recurrent network, repeat vector, time distributed network
    post_layer = Input(shape=(post_maxlen, vocab_size))
    encoder_rnn = LSTM(
        n_hidden,
        dropout=dropout,
        recurrent_dropout=recurrent_dropout
    )(post_layer)
    repeat_encode = RepeatVector(comment_maxlen)(encoder_rnn)
    dense_layer = TimeDistributed(Dense(vocab_size))(repeat_encode)
    regularized_layer = ActivityRegularization(l2=1)(dense_layer)
    softmax_layer = Activation('softmax')(regularized_layer)
    model = Model([post_layer], [softmax_layer])
    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )
    print (model.summary())

    # model checkpoint
    checkpoint_path = '{base}/model/cp.ckpt'.format(base=cwd)
    checkpoint_dir = os.path.dirname(checkpoint_path)
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
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
        callbacks = [cp_callback]
    )

    # save model
    save_model(
        model,
        '{base}/model/chatbot.h5'.format(base=cwd),
        overwrite=True,
        include_optimizer=True,
        period=checkpoint_period
    )

def encode(sentence, maxlen,vocab_size, word2idx):
    '''

    convert words to indices

    '''

    indices = np.zeros((maxlen, vocab_size))
    for i, w in enumerate(nltk.word_tokenize(sentence)):
        print('i: {i}, w: {w}'.format(i=i, w=w))
        if i == maxlen: break
        indices[i, word2idx[w]] = 1
    return indices

def create_posts(posts, vocab_size, post_maxlen, word2idx):
    '''

    vectorize posts using maximum post length.

    '''

    post_idx = np.zeros(shape=(len(posts),post_maxlen, vocab_size))
    for p in range(len(posts)):
        post = encode(posts[p], post_maxlen,vocab_size, word2idx)
        post_idx[p] = post
    return post_idx

def create_comments(comments, vocab_size, comment_maxlen):
    '''

    vectorize posts using maximum comment length.

    '''

    comment_idx = np.zeros(shape=(len(comments), comment_maxlen, vocab_size))
    for c in range(len(comments)):
        comment = encode(comments[c], comment_maxlen,vocab_size)
        comment_idx[c] = comment
    return comment_idx