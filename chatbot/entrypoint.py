#!/usr/bin/python

'''

upload.py, upload specified data to mongodb endpoint.

'''

import os
from nltk import tag, word_tokenize
from nmt_chatbot.inference import interactive

original_cwd = os.getcwd()
print("\n\nStarting interactive mode (first response will take a while):")

# QAs
while True:
    # prompt input
    question = input('\n> ')

    # penn-tree: tokenize + parts of speech
    sent = word_tokenize(question)
    tagged_words = tag.pos_tag(sent)

    # generate response
    inference_internal = interactive(question)
    answers = inference_internal(question)[0]

    # display response
    if answers is None:
        print(colorama.Fore.RED + "! Question can't be empty" + colorama.Fore.RESET)
    else:
        print('{response}'.format(response=answers['answers'][answers['best_index']]))

os.chdir(original_cwd)
