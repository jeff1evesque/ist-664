#!/usr/bin/python

'''

upload.py, upload specified data to mongodb endpoint.

'''

import os
from nltk.corpus import treebank
from nmt_chatbot.inference import interactive

original_cwd = os.getcwd()

# QAs
while True:
    question = input('\n> ')
    print(interactive(question))
    inference_internal = interactive(question)
    answers = inference_internal(question)[0]
    if answers is None:
        print(colorama.Fore.RED + "! Question can't be empty" + colorama.Fore.RESET)
    else:
        print('{response}'.format(response=answers['answers'][answers['best_index']]))

os.chdir(original_cwd)
