#!/usr/bin/python

'''

train.py, train LSTM model

'''

import os
import joblib
import numpy as np
import tensorflow as tf
from keras.models import Model, save_model
from keras.layers import Input, LSTM, Dense
from os import path, makedirs
from keras.models import model_from_json
from datetime import datetime


def train(
    posts,
    comments,
    cwd,
    epochs=1,
    batch_size=64,
    split=0.2,
    checkpoint=False,
    checkpoint_period=1
):
    #
    # local variables
    #
    # Note: posts, comments, and nb_samples should be the same length.
    #
    post_chars = set()
    comment_chars = set()
    post_lookup_index = {}
    post_lookup_char = {}
    comment_lookup_char = {}
    comment_lookup_index = {}
    nb_samples = int(len(posts) / 1000)

    # split sentences by chararacters
    for line in range(nb_samples):
	    #
	    # <sent>, start of the sentence
        # </sent>, end of the sentence
	    #
        post_line = posts[line]
        comment_line = '<sent>' + comments[line] + '</sent>'

        for char in post_line:
            if (char not in post_chars):
                post_chars.add(char)

        for char in comment_line:
            if (char not in comment_chars):
                comment_chars.add(char)

    comment_chars = sorted(list(comment_chars))
    post_chars = sorted(list(post_chars))

    for k, v in enumerate(post_chars):
        post_lookup_index[k] = v
        post_lookup_char[v] = k

    for k, v in enumerate(comment_chars):
        comment_lookup_char[k] = v
        comment_lookup_index[v] = k

    max_len_posts = max([len(line) for line in posts])
    max_len_comments = max([len(line) for line in comments])

    tokenized_posts = np.zeros(shape=(
        nb_samples,
        max_len_posts,
        len(post_chars)
    ), dtype='float32')
    tokenized_comments = np.zeros(shape=(
        nb_samples,
        max_len_comments,
        len(comment_chars)
    ), dtype='float32')
    target_data = np.zeros((
        nb_samples,
        max_len_comments,
        len(comment_chars)
    ),dtype='float32')

    # vectorize post and comments
    for i in range(nb_samples):
        for k, char in enumerate(posts[i]):
            tokenized_posts[i, k, post_lookup_char[char]] = 1

        for k, char in enumerate(comments[i]):
            tokenized_comments[i, k, comment_lookup_index[char]] = 1

            # decoder_target_data will be ahead by one timestep and will not include the start chararacter.
            if k > 0:
                target_data[i, k-1, comment_lookup_index[char]] = 1

    # encoder
    encoder_input = Input(shape=(None, len(post_chars)))
    encoder_LSTM = LSTM(256, return_state = True)
    encoder_outputs, encoder_h, encoder_c = encoder_LSTM (encoder_input)
    encoder_states = [encoder_h, encoder_c]

    # decoder
    decoder_input = Input(shape=(None, len(comment_chars)))
    decoder_LSTM = LSTM(256, return_sequences=True, return_state = True)
    decoder_out, _ , _ = decoder_LSTM(decoder_input, initial_state=encoder_states)
    decoder_dense = Dense(len(comment_chars), activation='softmax')
    decoder_out = decoder_dense (decoder_out)

    # checkpoint callback
    if checkpoint:
        cp = '{base}/model/cp--{date}.ckpt'.format(base=cwd, date=datetime.now())
        cp_dir = os.path.dirname(cp)
        cp_callback = [tf.keras.callbacks.ModelCheckpoint(
            cp_dir,
            save_weights_only=True,
            period=checkpoint_period,
            verbose=1
        )]
    else:
        cp_callback = False

    # generate model
    model = Model(inputs=[encoder_input, decoder_input], outputs=[decoder_out])
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
    model.fit(
        x=[tokenized_posts, tokenized_comments], 
        y=target_data,
        batch_size=batch_size,
        epochs=epochs,
        validation_split=split,
        callbacks = cp_callback
    )

    # model directory
    if not path.exists('{base}/model'.format(base=cwd)):
        makedirs('{base}/model'.format(base=cwd))

    # save model
    save_model(
        model,
        '{base}/model/chatbot.h5'.format(base=cwd),
        overwrite=True,
        include_optimizer=True
    )
