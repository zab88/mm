import pymysql
from settings import *
from stdnum import iban
from pandas import DataFrame


def fill_db(fields_dict, file_name):
    conn = pymysql.connect(host='localhost', port=3306, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
    cur = conn.cursor()

    sql = "INSERT INTO  invoice_doc_train (id, file_name) VALUES (NULL, %s)"
    cur.execute(sql, (file_name,))

    # get last id
    last_invoice_id = cur.lastrowid

    sql = "INSERT INTO invoice_fields_train (id, invoice_train_id, name, value, use_or_not) " \
          "VALUES (NULL, %s, %s, %s, '1')"
    for name, value in fields_dict.items():
        cur.execute(sql, (last_invoice_id, name, value))
    conn.commit()

    cur.close()
    conn.close()


def get_values_iban(limit=0):
    sql = "SELECT t0.file_name, t1.value, t2.value, t1.invoice_train_id " \
          "FROM invoice_fields_train t1, invoice_fields_train t2, invoice_doc_train t0 " \
          "WHERE t1.invoice_train_id = t2.invoice_train_id AND t1.invoice_train_id = t0.id " \
          "AND t1.name = 'supplier_country_short' AND t2.name = 'doc_pay_iban'"
    if limit:
        sql += ' LIMIT {}'.format(limit)

    conn = pymysql.connect(host='localhost', port=3306, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    iban_values = []
    for r in res:
        if len(r[2]) < 5:
            continue
        check_sum = iban.calc_check_digits(r[1] + 'xx' + r[2])
        # print(check_sum)
        doc_pay_iban = str(r[1]) + str(check_sum) + str(r[2])
        iban_values.append({'file_name':r[0], 'doc_pay_iban': doc_pay_iban.upper()})
        # print(r[0], r[1], r[2])
    return iban_values


def get_correct_values(fields, limit=0):
    sql = "select d.file_name, f.name, f.value, d.id from invoice_doc_train d " \
          "LEFT JOIN invoice_fields_train f ON d.id = f.invoice_train_id " \
          "WHERE f.name IN ({}) AND f.use_or_not > 0 ORDER BY d.id ".format("'" + "','".join(fields) + "'")
    if limit:
        sql += ' LIMIT {} '.format(limit * len(fields))

    conn = pymysql.connect(host='localhost', port=3306, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    values = []
    for r in res:
        if r[0] in ['supplier_name', 'doc_customer_ref']:
            values.append({'file_name': r[0], str(r[1]): str(r[2]).upper().replace(',', '')})
        else:
            values.append({'file_name': r[0], str(r[1]): str(r[2]).upper()})
    return values


def get_correct_values_df(fields, limit=0):
    sql = "select d.file_name, f.name, f.value, d.id from invoice_doc_train d " \
          "LEFT JOIN invoice_fields_train f ON d.id = f.invoice_train_id" \
          "WHERE f.name IN ({}) ORDER BY d.id ".format("'" + "','".join(fields) + "'")
    if limit:
        sql += ' LIMIT {} '.format(limit * len(fields))

    conn = pymysql.connect(host='localhost', port=3306, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)

    df = DataFrame(cur.fetchall())
    df.columns = cur.keys()
    return df


def fill_postal_no():
    conn = pymysql.connect(host='localhost', port=3306, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
    cur = conn.cursor()
    with open(HOME_DIR + '/helpers/no_postal_codes.csv', 'r', encoding='utf-8') as f:
        next(f)  # first line skip
        for line in f:
            sql = "INSERT INTO `postal_no` (`id`, `postal`, `place`, `state`, `county`) VALUES (NULL, %s, %s, %s, %s)"
            r = line.split(',')
            cur.execute(sql, (r[0], r[1], r[2], r[3]))
    conn.commit()
