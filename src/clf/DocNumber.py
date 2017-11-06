import datetime
from src.clf.GeneralClf import GeneralClf


class DocNumber(GeneralClf):
    SQL_FIELD = 'doc_number'

    @staticmethod
    def is_candidate(s):
        if any(not x.isdigit() for x in s):
            return False
        if len(s) < 4:
            return False
        s_cleaned = s[:]
        return s_cleaned
        # s_cleaned = s.replace('/', '').replace('-', '')
        # if s_cleaned.isdigit() and len(s_cleaned) >= (len(s)-1):
        #     return s_cleaned
        # return False

    @staticmethod
    def is_valid(s):
        return True
