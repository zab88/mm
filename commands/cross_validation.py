from helpers.train_helper import get_XY
from sklearn.model_selection import train_test_split
from settings import *


print("{:20}{:10}{:10}{:10}{:10}".format('field', 'documents', 'test', 'correct', 'accuracy'))
for field_name in IMPLEMENTED_FIELDS:
    # 1. extracting all data
    X, Y, Z, found_num, total_num = get_XY(field_name)

    # 2. split on test and train
    Z_train, Z_test, Zz_train, Zz_test = train_test_split(list(set(Z)), list(set(Z)), test_size=0.33)
    X_train, X_test, Y_train, Y_test, Z_doc_train, Z_doc_test = [], [], [], [], [], []

    for k, el in enumerate(Z):
        if el in Z_train:
            X_train.append(X[k])
            Y_train.append(Y[k])
            Z_doc_train.append(el)
        if el in Z_test:
            X_test.append(X[k])
            Y_test.append(Y[k])
            Z_doc_test.append(el)
    documents_tt_num = len(list(set(Z)))

    # 3. train
    clf_class_name = FIELD2CLF[field_name]
    clf_class = clf_class_name()
    clf_class.fit(X_train, Y_train)

    # 4. test
    correct = 0
    incorrect = 0
    already_predicted_docs = []
    doc_val = {}
    for k, el in enumerate(X_test):
        predicted = clf_class.predict(X_test[k])
        if predicted == Y_test[k]:
            correct += 1
        else:
            incorrect += 1
        if predicted == Y_test[k] and Y_test[k] == 1:
            already_predicted_docs.append(Z_doc_test[k])
        # print(X_test[k], Y_test[k])
            # if Z_test[k] not in doc_val:
            #     doc_val[Z_test[k]] =

    # print('tested docs num = {}, predicted docs num = {}'.format(len(list(set(Z_test))), len(list(set(already_predicted_docs)))))
    # print("correct: {}, incorrect: {}, from documents: {}".format(correct, incorrect, found_num))
    # print('\r\n\r\n')

    c_test = len(list(set(Z_test)))
    c_correct = len(list(set(already_predicted_docs)))
    print("{:20}{:10}{:10}{:10}{}".format(field_name, str(found_num), str(c_test), str(c_correct), float(c_correct)/float(c_test)))
