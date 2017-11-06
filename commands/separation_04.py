from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import glob, os
from helpers.xml_helper import read_xml_model
from settings import *
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
import numpy as np


def only_alpha(s):
    return ''.join([x if x.isalpha() else '' for x in s])

def to_skip(abn_file):
    with open(abn_file, 'r', encoding="utf-8") as f:
        content = f.read()
    if '<Comment>Multiple invoice</Comment>' in content:
        print('skipped', abn_file)
        return True
    return False

features_X, answers_Y, bad_docs = [], [], []
file_names = []
for xml_path in glob.glob(HOME_DIR + '/data_test/xml_models/*.xml'):
    model = read_xml_model(xml_path)
    if len(model.tokens) < 10:
        bad_docs.append(xml_path)
        continue
    abn_file = os.path.basename(xml_path).replace('..xml', '.abn')
    # print(abn_file)
    is_attachment = True if os.path.isfile(HOME_DIR + '/Testdata/{}'.format(abn_file)) else False
    if is_attachment:
        if to_skip(HOME_DIR + '/Testdata/{}'.format(abn_file)):
            continue

    # extract features
    avg_height = [x.h for x in model.tokens]
    avg_height = sum(avg_height) / (1.5 * len(model.tokens))
    # txt = ' '.join([only_alpha(x.txt) for x in model.tokens if x.h >= avg_height])
    txt = ' '.join([only_alpha(x.txt) for x in model.tokens])

    features_X.append(txt)
    answers_Y.append(is_attachment)
    file_names.append((os.path.basename(xml_path), is_attachment))

# train and check
vectorizer = TfidfVectorizer()
# vectorizer = CountVectorizer()
X = vectorizer.fit_transform(features_X)
clf_rf = RandomForestClassifier()
# clf_rf = svm.SVC()


if False:
    scores = cross_val_score(clf_rf, X, answers_Y, cv=5)
    print(scores)
    print('bad docs', len(bad_docs))

if True:
    # X_train, X_test, Y_train, Y_test = train_test_split(X, answers_Y, test_size=0.2)
    X_train, X_test, Y_train_f, Y_test_f = train_test_split(X, file_names, test_size=0.3)
    Y_train = [x[1] for x in Y_train_f]
    Y_test = [x[1] for x in Y_test_f]
    clf_rf.fit(X_train, Y_train)

    correct = 0
    incorrect = 0
    for k, el in enumerate(X_test):
        predicted = clf_rf.predict(X_test[k])
        predicted2 = clf_rf.predict_proba(X_test[k])
        # print(predicted, '!', predicted2)
        if predicted == Y_test[k]:
            correct += 1
        else:
            incorrect += 1
            print(Y_test_f[k])
            print(predicted, '!', predicted2)

    print(correct, incorrect + correct, correct / (incorrect + correct))
