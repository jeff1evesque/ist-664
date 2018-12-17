#!/usr/bin/python

'''

run.py, apply chatbot.

'''

import os
cwd = os.getcwd()

# tokenize is required by the 'clf_bu' model
from pymongo import MongoClient
from nltk import tag, word_tokenize, tokenize
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
from sklearn.externals import joblib
from QuestionAnswerCMU.utility import (
    tokenizer,
    normalize_data,
    replace,
    penn_scale
)
import pickle
import sys


def main(op='generic'):
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
        replies = combined['replies']
        scores = combined['comments']
        model = train(posts, replies)

    elif op == 'generic':
        # import previously trained models
        clf_rf = joblib.load('{base}/QuestionAnswerCMU/model/random_forest.pkl'.format(base=cwd))

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
            prediction = clf_rf.predict([X_sentence])

            # generate response
            if prediction == '0':
                inference_internal = interactive(sentence)
                answers = inference_internal(sentence)[0]

                # display response
                if answers is None:
                    print(colorama.Fore.RED + "! Question can't be empty" + colorama.Fore.RESET)
                else:
                    print('{response}'.format(response=answers['answers'][answers['best_index']]))

    os.chdir(cwd)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--insert':
        main(op='insert')

    elif len(sys.argv) > 1 and sys.argv[1] == '--local':
        main(op='local')

    else:
        main(op='generic')
