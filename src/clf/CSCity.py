from src.clf.GeneralClf import GeneralClf
# from settings import *
import pymysql


class CSCity(GeneralClf):
    # SQL_FIELD = ['supplier_city', 'customer_city']
    cities = None

    @staticmethod
    def is_candidate(s):
        if any(x.isdigit() for x in s):
            return False
        s_cleaned = ''.join([x.upper() if x.isalpha() else '' for x in s])
        if len(s_cleaned) < 4:
            return False
        # if not s[0].isupper():
        #     return False
        if CSCity.cities is None:
            CSCity.cities = CSCity.get_cities_no_list()
            # print(CSCity.cities)
        # all in upper case
        if s_cleaned not in CSCity.cities:
            return False

        # print(s_cleaned)
        return s_cleaned

    @staticmethod
    def is_valid(s):
        return True

    @staticmethod
    def get_cities_no_list():
        _DB_NAME = 'invoiceai'
        _DB_USER = 'invoiceai'
        _DB_PASS = 'UzHTzLLhSqP23dBz'

        sql = "select DISTINCT place from postal_no "

        conn = pymysql.connect(host='localhost', port=3306, user=_DB_USER, passwd=_DB_PASS, db=_DB_NAME, charset='utf8')
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        values = []
        for r in res:
            values.append(r[0].upper())
        return values
