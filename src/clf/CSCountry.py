from src.clf.GeneralClf import GeneralClf


class CSCity(GeneralClf):
    SQL_FIELD = ['supplier_country', 'customer_country']

    @staticmethod
    def is_candidate(s):
        return "NO"

    @staticmethod
    def is_valid(s):
        return True
