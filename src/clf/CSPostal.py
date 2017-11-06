from src.clf.GeneralClf import GeneralClf
import pymysql


class CSPostal(GeneralClf):
    # SQL_FIELD = ['supplier_postal', 'customer_postal']
    postals = None

    @staticmethod
    def is_candidate(s):
        # if any(x.isalpha() for x in s):
        #     return False
        s_cleaned = ''.join([x if x.isdigit() else '' for x in s])
        if len(s_cleaned) != 4:
            return False
        if CSPostal.postals is None:
            CSPostal.postals = CSPostal.get_postal_no_list()
        if s_cleaned not in CSPostal.postals:
            return False
        return s_cleaned

    @staticmethod
    def is_valid(s):
        return True

    @staticmethod
    def get_postal_no_list():
        _DB_NAME = 'invoiceai'
        _DB_USER = 'invoiceai'
        _DB_PASS = 'UzHTzLLhSqP23dBz'

        sql = "select DISTINCT postal from postal_no "

        conn = pymysql.connect(host='localhost', port=3306, user=_DB_USER, passwd=_DB_PASS, db=_DB_NAME, charset='utf8')
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        values = []
        for r in res:
            values.append(r[0].upper())
        return values
