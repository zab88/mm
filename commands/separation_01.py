from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import glob, os
from helpers.xml_helper import read_xml_model
from settings import *
from sklearn.model_selection import cross_val_score
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
for xml_path in glob.glob(HOME_DIR + '/data_test/xml_models/*.xml'):
    model = read_xml_model(xml_path)
    if len(model.tokens) < 1:
        bad_docs.append(xml_path)
        continue
    abn_file = os.path.basename(xml_path).replace('..xml', '.abn')
    # print(abn_file)
    is_attachment = True if os.path.isfile(HOME_DIR + '/Testdata/{}'.format(abn_file)) else False
    if is_attachment:
        if to_skip(HOME_DIR + '/Testdata/{}'.format(abn_file)):
            continue

    # extract features
    txt = ' '.join([only_alpha(x.txt) for x in model.tokens])

    features_X.append(txt)
    answers_Y.append(is_attachment)

# train and check
vectorizer = TfidfVectorizer()
# vectorizer = CountVectorizer()
X = vectorizer.fit_transform(features_X)
clf_rf = RandomForestClassifier()
# clf_rf = svm.SVC()
scores = cross_val_score(clf_rf, X, answers_Y, cv=5)
print(scores)
print('bad docs', len(bad_docs))
# for k, el in enumerate(features_X):
#     print(answers_Y[k], features_X[k])

# idf = vectorizer.idf_
# non_ordered = dict(zip(vectorizer.get_feature_names(), idf))
# ordered = [(k, non_ordered[k]) for k in sorted(non_ordered, key=non_ordered.get, reverse=True)]
# for k, v in ordered:
#     print(k, v)

exit()
clf_rf.fit(X, answers_Y)
importances = clf_rf.feature_importances_
features_names = vectorizer.get_feature_names()
indices = np.argsort(importances)[::-1]
names_indices = [features_names[x] for x in indices]

for k, el in enumerate(names_indices):
    if k > 30:
        break
    print(names_indices[k], importances[indices][k])
