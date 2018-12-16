#!/usr/bin/python

'''

run.py, apply chatbot.

'''

import os
cwd = os.getcwd()

from nltk import tag, word_tokenize
from chatbot.nmt_chatbot.inference import interactive
from sklearn.externals import joblib
from QuestionAnswerCMU.utility import tokenizer, normalize_data
import pickle

## import previously trained models
clf_rf = joblib.load('{base}/QuestionAnswerCMU/model/random_forest.pkl'.format(base=cwd))

print("\n\nStarting interactive mode (first response will take a while):")

# QAs
while True:
    # prompt input
    question = input('\n> ')

    # tokenize + parts of speech
    pos = tokenizer(question)

    # normalize question
    X_question = normalize_data(pos, stop_gap=40)
    print(X_question)

    print(clf_rf.predict(X_question))

    # generate response
    inference_internal = interactive(question)
    answers = inference_internal(question)[0]

    # display response
    if answers is None:
        print(colorama.Fore.RED + "! Question can't be empty" + colorama.Fore.RESET)
    else:
        print('{response}'.format(response=answers['answers'][answers['best_index']]))

os.chdir(cwd)
