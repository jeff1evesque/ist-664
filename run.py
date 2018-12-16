#!/usr/bin/python

'''

run.py, apply chatbot.

'''

import os
cwd = os.getcwd()

from nltk import tag, word_tokenize
from chatbot.nmt_chatbot.inference import interactive
from sklearn.externals import joblib
from QuestionAnswerCMU.utility import tokenizer, normalize_data, replace, penn_scale
import pickle

## import previously trained models
clf_rf = joblib.load('{base}/QuestionAnswerCMU/model/random_forest.pkl'.format(base=cwd))

print("\n\nStarting interactive mode (first response will take a while):")

# QAs
while True:
    # prompt input
    sentence = input('\n> ')

    # tokenize + parts of speech
    pos = tokenizer(sentence)

    # convert pos to numeric
    sentence_pos = [penn_scale().get(item,item) for item in pos]

    # normalize question
    X_sentence = normalize_data(sentence_pos, stop_gap=40)

    # check if question
    prediction = clf_rf.predict([X_sentence])

    # generate response
    if prediction == '1':
        inference_internal = interactive(sentence)
        answers = inference_internal(sentence)[0]

        # display response
        if answers is None:
            print(colorama.Fore.RED + "! Question can't be empty" + colorama.Fore.RESET)
        else:
            print('{response}'.format(response=answers['answers'][answers['best_index']]))

os.chdir(cwd)
