#!/usr/bin/python

'''

entrypoint.py, apply chatbot.

'''

import os
from nltk import tag, word_tokenize
from nmt_chatbot.inference import interactive
from sklearn.externals import joblib

## import previously trained models
rf = joblib.load('QuestionAnswerCMU/model/random_forrest.pkl')

original_cwd = os.getcwd()
print("\n\nStarting interactive mode (first response will take a while):")

# QAs
while True:
    # prompt input
    question = input('\n> ')

    # penn-tree: tokenize + parts of speech
    sent = word_tokenize(question)
    tagged_words = tag.pos_tag(sent)
    pos = [x[1] for x in pos if x[1] and x[1] in penn_scale]

    # generate response
    inference_internal = interactive(question)
    answers = inference_internal(question)[0]

    # display response
    if answers is None:
        print(colorama.Fore.RED + "! Question can't be empty" + colorama.Fore.RESET)
    else:
        print('{response}'.format(response=answers['answers'][answers['best_index']]))

os.chdir(original_cwd)
