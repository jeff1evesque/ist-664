#!/usr/bin/python

'''

run.py, apply chatbot.

'''

import os
cwd = os.getcwd()

# tokenize is required by the 'clf_bu' model
from nltk import tag, word_tokenize, tokenize
from nltk.tokenize import TreebankWordTokenizer, RegexpTokenizer

# general requirements
import joblib
from chatbot.nmt_chatbot.inference import interactive
from QuestionAnswerCMU.utility import (
    tokenizer,
    normalize_data,
    replace,
    penn_scale,
    qa_model
)
from StackOverflow.utility import tokenize, so_model

# local variables
client='jimmy'

# interative session
print("\n\nStarting interactive mode (first response will take a while):")
while True:
    # prompt input
    sentence = input('\n> ')

    # tokenize + parts of speech
    pos = tokenizer(sentence)

    # convert pos to numeric
    sentence_pos = replace(pos, penn_scale())

    # normalize question
    X_sentence = normalize_data(sentence_pos, stop_gap=40)

    # check if question
    prediction = qa_model(cwd).predict([X_sentence])

    # generate response
    if prediction == '0':
        inference_internal = interactive(sentence)
        answers = inference_internal(sentence)[0]

        # display response
        if answers is None:
            print(colorama.Fore.RED + "! Question can't be empty" + colorama.Fore.RESET)
        elif answers['best_score'] < 15:
            print('hey {name}, maybe checkout {url}'.format(
                name=client,
                url=so_model(cwd).predict([sentence])
            ))
        else:
            print('{response}'.format(response=answers['answers'][answers['best_index']]))

os.chdir(cwd)
