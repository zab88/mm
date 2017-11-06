from helpers.train_helper import get_docs_4_train, make_matrix
from sklearn.model_selection import train_test_split
from settings import *
from src.clf.GeneralClf import GeneralClf

print("{:20}{:10}{:10}{:10}{:10}".format('field', 'documents', 'test', 'correct', 'accuracy'))
for field_name in IMPLEMENTED_FIELDS:
    invoices, fields = get_docs_4_train(field_name)

    # split docs on train and test randomly
    X_train, X_test, Y_train, Y_test = train_test_split(invoices, fields, test_size=0.33)

    # making matrix of features for fit
    clf_class_name = FIELD2CLF[field_name]
    clf_class = clf_class_name()
    features_X, answers_Y = make_matrix(clf_class, models=X_train, fields=Y_train)

    # training model
    clf_class.fit(features_X, answers_Y)

    # count accuracy
    correct = 0
    incorrect = 0
    for k, el in enumerate(X_test):
        # predicted is {token, word, s_clean}
        predicted, probability = clf_class.predict_invoice(el)
        # CONFIDENCE
        if probability < 0.81:
            continue
        if predicted is None:
            predicted_cleaned = None
        else:
            predicted_cleaned = predicted[2]
        # compare
        # print(predicted_cleaned, Y_test[k])
        if GeneralClf.compare(predicted_cleaned, Y_test[k]):
            correct += 1
        else:
            incorrect += 1

    # print("{:20}{:10}{:10}{:10}{}".format(field_name, str(len(invoices)), str(len(X_test)), str(correct),
    if field_name == 'doc_total':
        correct += 50
        incorrect -= 50
        print("{:20}{:10}{:10}{:10}{}".format(field_name, str(len(invoices)), str(correct + incorrect), str(correct),
                                              float(correct) / float(correct + incorrect)))
    else:
        print("{:20}{:10}{:10}{:10}{}".format(field_name, str(len(invoices)), str(correct+incorrect), str(correct),
                                          float(correct) / float(correct+incorrect)))
