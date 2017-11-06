from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import glob, os
from settings import *
from helpers.xml_helper import read_xml_model
import copy
import matplotlib.pyplot as plt
import numpy as np


# loading clfs
clf_classes, clf_names = [], []
for clf_file in glob.glob(HOME_DIR + '/trained_classes/*.pkl'):
    clf_name = os.path.basename(clf_file).replace('.pkl', '')
    clf_class = joblib.load(clf_file)
    clf_classes.append(copy.copy(clf_class))
    clf_names.append(clf_name)
# print(clf_names)
# exit()

features_X, answers_Y, bad_docs = [], [], []
for xml_path in glob.glob(HOME_DIR + '/data_test/xml_models/*.xml'):
    model = read_xml_model(xml_path)
    if len(model.tokens) < 1:
        bad_docs.append(xml_path)
        continue
    # if len(features_X) > 30:
    #     break
    abn_file = os.path.basename(xml_path).replace('..xml', '.abn')
    # print(abn_file)
    is_attachment = True if os.path.isfile(HOME_DIR + '/Testdata/{}'.format(abn_file)) else False

    # create features
    new_feature = []
    for k, clf in enumerate(clf_classes):
        predicted = clf.predict_invoice(model)[0]
        # print(predicted)
        if predicted is None:
            new_feature.append(0)
        else:
            new_feature.append(1)
    # exit()

    print(new_feature)
    features_X.append(new_feature[:])
    answers_Y.append(is_attachment)


# train and check
clf_rf = RandomForestClassifier()
# clf_rf = svm.SVC()
scores = cross_val_score(clf_rf, features_X, answers_Y, cv=5)
print(scores)
print('bad docs', len(bad_docs))


clf_rf.fit(features_X, answers_Y)
importances = clf_rf.feature_importances_
print(importances)
std = np.std([tree.feature_importances_ for tree in clf_rf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

names_indices = [clf_names[x] for x in indices]

# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
# plt.bar(range(len(importances)), importances[indices], color="r", yerr=std[indices], align="center")
plt.bar(range(len(importances)), importances[indices], color="r")  #  yerr=std[indices], align="center")
plt.xticks(range(len(importances)), names_indices, rotation=90)
# plt.gcf().subplots_adjust(bottom=0.43)
plt.tight_layout()
plt.xlim([-1, len(importances)])
plt.show()
