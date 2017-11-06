from src.clf.GeneralClf import GeneralClf


class CSOrg(GeneralClf):
    # SQL_FIELD = ['supplier_org', 'customer_org']

    @staticmethod
    def is_candidate(s):
        s_cleaned = ''.join([x if x.isdigit() else '' for x in s])
        if len(s_cleaned) != 9:
            return False
        return s_cleaned

    @staticmethod
    def is_valid(s):
        return True
