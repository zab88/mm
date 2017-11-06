from helpers.train_helper import get_docs_4_train, make_matrix
from sklearn.externals import joblib
from settings import *

for field_name in IMPLEMENTED_FIELDS:
    invoices, fields = get_docs_4_train(field_name)

    # split docs on train and test randomly
    # X_train, X_test, Y_train, Y_test = train_test_split(invoices, fields, test_size=0.33)

    # making matrix of features for fit
    clf_class_name = FIELD2CLF[field_name]
    clf_class = clf_class_name()
    features_X, answers_Y = make_matrix(clf_class, models=invoices, fields=fields)

    # training model
    clf_class.fit(features_X, answers_Y)

    # saving trained .pkl
    joblib.dump(clf_class, HOME_DIR + os.sep + 'trained_classes' + os.sep + field_name + '.pkl')
    print("{} trained and saved".format(field_name))
