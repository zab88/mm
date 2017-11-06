from stdnum import iban
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.feature_extraction.text import CountVectorizer
from src.clf.GeneralClf import GeneralClf


class DocPayIban(GeneralClf):
    SQL_FIELD = 'doc_pay_iban'


    @staticmethod
    def is_candidate(s):
        s_cleaned = ''.join([x for x in s if x.isalpha() or x.isdigit()])
        if len(s_cleaned) > 15:
            return False
        if len(s_cleaned) < 11:
            return False
        # next condition only for iban
        if s_cleaned[:2].isalpha():
            if len(s_cleaned) < 15:
                s_cleaned = s_cleaned[2:]
            else:
                s_cleaned = s_cleaned[4:]

        if not s_cleaned.isdigit():
            return False
        s_cleaned = s_cleaned.upper()
        return s_cleaned


    @staticmethod
    def is_valid(s):
        # return iban.is_valid(s)
        return True
