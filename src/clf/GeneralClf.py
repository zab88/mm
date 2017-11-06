from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from src.TokenModel import TokenModel
# from settings import *


class GeneralClf:
    TYPE_CLF_RF = 0
    TYPE_CLF_KNN = 1
    TYPE_CLF_SVM = 2
    TYPE_CLF_SVM_LINE = 3
    TYPE_CLF_GNB = 4

    MAX_VALUABLE_DISTANCE = 1200

    @classmethod
    def get_candidates(cls, model):
        candidates = []
        field_name = cls.SQL_FIELD
        for word in model.words:
            for k, token in enumerate(word.tokens):
                cleaned_token = cls.is_candidate(token.txt)
                # print(token.txt, cleaned_token)
                # print(token.txt)
                if cleaned_token:
                    candidates.append([token, word, cleaned_token, field_name, (k, 0)])
            # merge 2
            for k, el in enumerate(word.tokens):
                if k + 1 >= len(word.tokens):
                    break
                cleaned_token = cls.is_candidate(word.tokens[k].txt + word.tokens[k + 1].txt)
                if cleaned_token:
                    candidates.append([None, word, cleaned_token, field_name, (k, 1)])
            # merge 3
            for k, el in enumerate(word.tokens):
                if k + 2 >= len(word.tokens):
                    break
                cleaned_token = cls.is_candidate(
                    word.tokens[k].txt + word.tokens[k + 1].txt + word.tokens[k + 2].txt)
                if cleaned_token:
                    candidates.append([None, word, cleaned_token, field_name, (k, 2)])
            # merge 4
            for k, el in enumerate(word.tokens):
                if k+3 >= len(word.tokens):
                    break
                cleaned_token = cls.is_candidate(
                    word.tokens[k].txt + word.tokens[k+1].txt + word.tokens[k+2].txt + word.tokens[k+3].txt)
                if cleaned_token:
                    candidates.append([None, word, cleaned_token, field_name, (k, 3)])
        return candidates

    @staticmethod
    def get_features(word_model):
        # print(word_model.txt)
        return word_model.txt

    @staticmethod
    def get_spatial_features(model, candidate):
        # measure spatial distance between all tokens
        features_dict = {}
        start_token = candidate[1].tokens[candidate[4][0]]
        for t in model.tokens:
            dist = start_token - t
            if abs(dist) > GeneralClf.MAX_VALUABLE_DISTANCE:
                continue
            feature_word = ''.join([x for x in t.txt if x.isalpha()])

            # saving only nearest
            if feature_word in features_dict:
                old_dist = features_dict[feature_word]
                if abs(old_dist) < abs(dist):
                    continue
            features_dict[feature_word] = dist
        ff = {}
        for k, val in sorted(features_dict.items(), key=lambda item: (item[1], item[0])):
            ff[k] = val
            if len(ff) >= 5:
                break
        print(candidate[2], ff)
        # return features_dict
        return ff

    @staticmethod
    def get_features_advanced(model, candidate):  # candidate is {token/None, word, s_cleaned, feature_name, offsets}
        # select type of features for each field
        # print(candidate[2])
        if False:
            return GeneralClf.get_spatial_features(model, candidate)
        if candidate[3] not in ['doc_numberr', 'customer_postall']:
            text_features = GeneralClf.get_features(candidate[1])
            upper_tokens = TokenModel.get_upper_tokens(candidate[1].tokens[candidate[4][0]], model.tokens)
            # print([x.txt for x in upper_tokens])
            return text_features + ' ' + ' '.join([x.txt for x in upper_tokens])

        block_num = candidate[1].tokens[0].block_num
        block = None
        for b in model.blocks:
            if b.block_num == block_num:
                block = b
                break
        print('WW: ' + candidate[1].txt)
        print('BB: ' + block.txt)
        return block.txt

    def fit(self, features_X, answers_Y, type_clf=None):
        self.type_clf = type_clf
        # using bag of words approach
        if True:
            self.vectorizer = CountVectorizer()
        # using dict
        if False:
            self.vectorizer = DictVectorizer()

        X = self.vectorizer.fit_transform(features_X)
        # vectorizer.build_analyzer()

        # type clf selection
        if type_clf == GeneralClf.TYPE_CLF_GNB:
            self.clf_rf = GaussianNB()
        elif type_clf == GeneralClf.TYPE_CLF_KNN:
            self.clf_rf = KNeighborsClassifier()
        elif type_clf == GeneralClf.TYPE_CLF_SVM:
            self.clf_rf = svm.SVC() # default kernel RBF (Radial basis function kernel)
        elif type_clf == GeneralClf.TYPE_CLF_SVM_LINE:
            self.clf_rf = svm.SVC(kernel="linear", C=0.025)
        else:
            # Random Forest
            self.type_clf = GeneralClf.TYPE_CLF_RF
            self.clf_rf = RandomForestClassifier()

        self.clf_rf.fit(X, answers_Y)  # .toarray()
        # if not DEBUG:
        #     print('Random Forest trained!')

    def predict(self, txt):
        X_predict = self.vectorizer.transform([txt])
        predicted = self.clf_rf.predict(X_predict)[0]
        if predicted > 0:
            return True
        return False

    def predict_invoice(self, model):
        candidates = self.get_candidates(model)  # list of (token/None, word, cleaned_token)
        best_candidate = None
        best_candidate_prob = 0
        for candidate in candidates:
            # txt = GeneralClf.get_features(candidate[1])
            txt = GeneralClf.get_features_advanced(model, candidate)
            feature = self.vectorizer.transform([txt])
            predicted = self.clf_rf.predict_proba(feature)
            prob = predicted[0][1]
            if prob > 0.50:  # 0.55
                if prob > best_candidate_prob:
                    best_candidate = candidate
                    best_candidate_prob = prob
        return best_candidate, best_candidate_prob

    @staticmethod
    def compare(val1, val2, field_type=None):
        if field_type == 'doc_total':
            if not str(val1).replace('.', '', 1).isdigit():
                return False
            if not str(val2).replace('.', '', 1).isdigit():
                return False
            return float(val1) == float(val2)
        if str(val1).upper() == str(val2).upper():
            return True
        return False
