import datetime
from src.clf.GeneralClf import GeneralClf


class DocTotal(GeneralClf):
    SQL_FIELD = 'doc_total'

    @staticmethod
    def is_candidate(s):
        if ',' not in s and '.' not in s:
            return False
        if any(x.isalpha() for x in s):
            return False
        s_cleaned = ''.join([x if x.isdigit() else ' ' for x in s])
        s_cleaned = s_cleaned.strip()
        if len(s_cleaned) < 1:
            return False
        # print('!!!', s_cleaned)
        s_cleaned = s_cleaned.split()
        # should end with cents. That rule probably should be deleted in future
        # print(s_cleaned)
        if len(s_cleaned[-1]) != 2 or len(s_cleaned) < 2:
            return False
        s_cleaned = ''.join(s_cleaned[:-1]) + '.' + s_cleaned[-1]
        # print(s)
        try:
            tt = float(s_cleaned)
            if tt > 1000000:
                return False
            return s_cleaned
        except ValueError:
            return False

    @staticmethod
    def is_valid(s):
        return True

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
        if best_candidate is not None:
            return best_candidate, best_candidate_prob

        candidates = self.get_candidates(model)  # list of (token/None, word, cleaned_token, feature_name, offsets)
        if len(candidates) < 1:
            return None, 0
        best_candidate = None
        best_candidate_prob = 0
        best_candidates = []
        y_current = -1
        for candidate in candidates:
            token = candidate[1].tokens[candidate[4][0]]
            tokens = candidate[1].tokens[candidate[4][0]:candidate[4][0]+candidate[4][1]]
            # print(''.join([x.txt for x in tokens]))
            if y_current < token.y:
                best_candidate = candidate
                best_candidate_prob = 1
        # for candidate in candidates:
        #     # txt = GeneralClf.get_features(candidate[1])
        #     txt = GeneralClf.get_features_advanced(model, candidate)
        #     feature = self.vectorizer.transform([txt])
        #     predicted = self.clf_rf.predict_proba(feature)
        #     prob = predicted[0][1]
        #     if prob > 0.55:
        #         if prob > best_candidate_prob:
        #             best_candidate = candidate
        #             best_candidate_prob = prob
        return best_candidate, best_candidate_prob
