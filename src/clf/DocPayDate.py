import datetime
from src.clf.GeneralClf import GeneralClf


class DocPayDate(GeneralClf):
    SQL_FIELD = 'doc_pay_date'

    MONTHS_DICT = [
        ['jan', 'febr', 'mars', 'april', 'mai', 'juni', 'juli', 'aug', 'sept', 'okt', 'nov', 'des'],
        ['januar', 'februar', 'mars', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november',
         'desember'],
        # italian
        ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre',
         'novembre', 'dicembre'],
        # spanish
        ['enero', 'feb', 'marzo', 'abr', 'mayo', 'jun', 'jul', 'agosto', 'set', 'oct', 'nov', 'dic']
    ]

    @staticmethod
    def is_candidate(date):
        s_cleaned = ''.join([x if x.isdigit() else ' ' for x in date])
        s_cleaned = s_cleaned.split()
        # ddmmyy
        if len(s_cleaned) == 1 and len(s_cleaned[0]) == 6 and s_cleaned[0].endswith('17'):
            s_cleaned = [s_cleaned[0][0:2], s_cleaned[0][2:4], s_cleaned[0][4:6]]
        if len(s_cleaned) != 3:
            return DocPayDate.is_candidate2(date)
        s_cleaned = '-'.join(s_cleaned)
        patterns = ['%Y-%m-%d', '%d-%m-%Y', '%d-%m-%y', '%y-%m-%d']
        results = []
        for p in patterns:
            try:
                date_obj = datetime.datetime.strptime(s_cleaned, p)
                results.append(date_obj.strftime('%Y-%m-%d'))
            except ValueError:
                # other pattern can be better
                pass
        if len(results) < 1:
            return False
        if len(results) == 1:
            return results[0]
        for r in results:
            if '2017' in r:
                return r
        return results[0]

    @staticmethod
    def is_candidate2(date):
        s_cleaned = ''.join([x if x.isdigit() or x.isalpha() else '' for x in date])
        if len(s_cleaned) < 7:
            return False
        if not s_cleaned[0].isdigit():
            return False
        if s_cleaned[1].isdigit():
            day = s_cleaned[:2]
            day_offset = 2
        else:
            day = '0' + str(s_cleaned[:1])
            day_offset = 1
        if not s_cleaned[-4:].isdigit():
            return False
        if not s_cleaned[day_offset:-4].isalpha():
            return False
        month_name_candidate = s_cleaned[2:-4].lower()
        for months in DocPayDate.MONTHS_DICT:
            for k, month_name in enumerate(months):
                if month_name.lower() == month_name_candidate:
                    month_number = '0' + str(k + 1) if k < 9 else str(k + 1)

                    result = "{}-{}-{}".format(s_cleaned[-4:], month_number, day)
                    # print(result)
                    return result
        return False

    @staticmethod
    def is_valid(s):
        return True

    def predict_invoice(self, model):
        candidates = self.get_candidates(model)  # list of (token/None, word, cleaned_token)
        best_candidate = None
        best_candidate_prob = 0
        clear_candidates = [x[2] for x in candidates]
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
        if len(list(set(clear_candidates))) == 2:
            min_date = min(clear_candidates)
            max_date = max(clear_candidates)
            best_candidate = list(filter(lambda x: x[2] == max_date, candidates))[0]
            # print(clear_candidates)

        return best_candidate, best_candidate_prob
