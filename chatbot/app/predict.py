#!/usr/bin/python

'''

predict.py, using loaded lstm model generate sequence.

'''

from keras.models import load_model


def predict(cwd, question):
    '''

    predict sequence response.

    '''

    model = load_model('{base}/model/chatbot.h5'.format(base=cwd))
    return model.predict(question)