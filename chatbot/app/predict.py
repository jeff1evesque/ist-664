#!/usr/bin/python

'''

predict.py, using loaded lstm model generate sequence.

'''

from keras.models import load_model
from joblib import load


def predict(cwd, question):
    '''

    predict sequence response.

    '''

    model = load_model('{base}/model/chatbot.h5'.format(base=cwd))
    return model.predict(decode(question), cwd=cwd)

def decode(indices, calc_argmax=True, cwd=''):
    '''

    convert indices to words.

    '''

    idx2word = load('{base}/model/idx2word.pkl'.format(base=cwd))
    if calc_argmax:
        indices = np.argmax(indices, axis=-1)
    return ' '.join(idx2word[x] for x in indices)