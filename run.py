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
from Reddit.nmt_chatbot.inference import interactive
from Reddit.app.train import train
from Reddit.app.insert import insert_dataset
from Reddit.app.select import select
from Reddit.app.predict import predict
from config import (
    mongos_endpoint,
    database,
    collection,
    data_directory,
    username,
    epochs,
    batch_size,
    split,
    n_hidden,
    post_maxlen,
    comment_maxlen,
    dropout,
    recurrent_dropout,
    checkpoint,
    checkpoint_period
)
from QuestionAnswerCMU.utility import (
    tokenizer,
    normalize_data,
    replace,
    penn_scale,
    qa_model
)
from StackOverflow.utility import tokenize, so_model

def main(op='generic'):
    '''
    application entrypoint.
    '''

    if op == 'insert':
        client = MongoClient(mongos_endpoint)
        insert_dataset(
            client,
            database,
            collection,
            '{base}/Reddit/{subdir}'.format(base=cwd, subdir=data_directory)
        )

    elif op == 'train':
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
        model = train(
            posts,
            comments,
            epochs=epochs,
            batch_size=batch_size,
            split=split,
            n_hidden=n_hidden,
            post_maxlen=post_maxlen,
            comment_maxlen=comment_maxlen,
            dropout=dropout,
            recurrent_dropout=recurrent_dropout,
            checkpoint=checkpoint,
            checkpoint_period=checkpoint_period,
            cwd=cwd
        )

    elif op == 'local':
        while True:
            # prompt input
            sentence = input('\n> ')

            # predicted sentence
            print(predict(sentence, cwd=cwd, post_maxlen=post_maxlen))

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

    elif len(sys.argv) > 1 and sys.argv[1] == '--train':
        main(op='train')

    elif len(sys.argv) > 1 and sys.argv[1] == '--local':
        main(op='local')

    else:
        main(op='generic')
