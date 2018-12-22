#!/usr/bin/python

'''
run.py, apply chatbot.
'''

import os
cwd = os.getcwd()

# tokenize is required by the 'clf_bu' model
from pymongo import MongoClient
from nltk import tag, word_tokenize, tokenize
from nltk.tokenize import TreebankWordTokenizer, RegexpTokenizer

# general requirements
import sys
import joblib
from chatbot.nmt_chatbot.inference import interactive
from chatbot.app.train import train
from chatbot.app.insert import insert
from chatbot.app.select import select
from chatbot.config import (
    mongos_endpoint,
    database,
    collection,
    data_directory
)
from QuestionAnswerCMU.utility import (
    tokenizer,
    normalize_data,
    replace,
    penn_scale,
    qa_model
)
from StackOverflow.utility import tokenize, so_model

# local variables
username='jimmy'

def main(op='generic'):
    '''
    application entrypoint.
    '''

    if op == 'insert':
        client = MongoClient(mongos_endpoint)
        insert(
            client,
            database,
            collection,
            '{base}/chatbot/{subdir}'.format(base=cwd, subdir=data_directory)
        )

    elif op == 'local':
        client = MongoClient(mongos_endpoint)
        results = select(client, database, collection)

        # combine sequence pairs
        combined = {}
        for doc in results.find():
            if doc['value']:
                for k, v in doc['value'].items():
                    if k in combined.keys():
                        combined[k] += v
                    else:
                        combined[k] = v

        posts = combined['posts']
        comments = combined['comments']
        scores = combined['scores']
        model = train(posts, comments, cwd=cwd)

    elif op == 'generic':
        # interative session
        print('\n\nStarting interactive mode (first response will take a while):')
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
                    print(colorama.Fore.RED + "Answer can't be empty!" + colorama.Fore.RESET)

                elif answers['best_score'] < 12:
                    print('hey {name}, maybe checkout {url}'.format(
                        name=username,
                        url=so_model(cwd).predict([sentence])
                    ))

                else:
                    print('{response}'.format(response=answers['answers'][answers['best_index']]))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--insert':
        main(op='insert')

    elif len(sys.argv) > 1 and sys.argv[1] == '--local':
        main(op='local')

    else:
        main(op='generic')
