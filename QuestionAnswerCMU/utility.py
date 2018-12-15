#!/usr/bin/python

'''

utility.py, helper function.

'''

def normalize_data(X_train, X_test, stop_gap=40, stop_value=0):
    ## get shape of dataframe
    rows_train, columns_train = X_train.shape
    rows_test, columns_test = X_test.shape

    train_delta = stop_gap - columns_train
    test_delta = stop_gap - columns_test

    ##
    ## columns fixed to 40:
    ##
    ## https://github.com/jeff1evesque/ist-664/issues/62#issuecomment-447223456
    ##
    if train_delta > 0 and train_delta <= stop_gap:
        for i in range(train_delta):
            X_train['filler-{}'.format(i)] = stop_value

    if test_delta > 0 and test_delta <= stop_gap:
        for i in range(test_delta):
            X_test['filler-{}'.format(i)] = stop_value

    if train_delta < 0:
        rem_list = [x for x in range(abs(columns_train))][train_delta:]
        X_train.drop(rem_list, axis=1, inplace=True)

    if test_delta < 0:
        rem_list = [x for x in range(abs(columns_train))][test_delta:]
        X_test.drop(rem_list, axis=1, inplace=True)

    ## return train + test
    return(X_train, X_test)