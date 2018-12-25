#!/usr/bin/python

'''

train.py, train LSTM model

'''

from keras.models import load_model


def predict(cwd, question):
    '''

    predict using loaded lstm model.

    '''

    model = load_model('{base}/model/chatbot.h5'.format(base=cwd))
    return model.predict(question)