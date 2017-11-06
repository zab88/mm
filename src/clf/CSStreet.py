from src.clf.GeneralClf import GeneralClf


class CSStreet(GeneralClf):
    SQL_FIELD = ['supplier_street', 'customer_street']

    @staticmethod
    def is_candidate(s):
        if not any(x.isalpha() for x in s):
            return False
        if not any(x.isdigit() for x in s):
            return False
        if not any(x.isupper() for x in s):
            return False
        s_cleaned = ''.join([x.upper() if x.isalpha() else '' for x in s])
        if len(s_cleaned) != 9:
            return False
        return s_cleaned

    @staticmethod
    def is_valid(s):
        return True
