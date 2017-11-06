import os
from src.clf.DocPayIban import DocPayIban
from src.clf.DocDate import DocDate
from src.clf.DocPayDate import DocPayDate
from src.clf.DocTotal import DocTotal
from src.clf.DocNumber import DocNumber
from src.clf.CustomerOrg import CustomerOrg
from src.clf.SupplierOrg import SupplierOrg
from src.clf.SupplierPostal import SupplierPostal
from src.clf.CustomerPostal import CustomerPostal
from src.clf.CustomerCity import CustomerCity
from src.clf.SupplierCity import SupplierCity
from src.clf.SupplierContact import SupplierContact
from src.clf.DocCustomerRef import DocCustomerRef


HOME_DIR = os.path.dirname(__file__)
DB_NAME = 'invoiceai'
DB_USER = 'invoiceai'
DB_PASS = 'UzHTzLLhSqP23dBz'

DEBUG = True

PATH_TESSDATA_PREFIX = 'C:/Program Files (x86)/Tesseract-OCR/tessdata/'

IMPLEMENTED_FIELDS = [
    'doc_date', 'doc_pay_date',
    # 'doc_total'
]
IMPLEMENTED_FIELDS = [
    'doc_number',
    'doc_pay_iban',  # 70%+
    'doc_date',  # 70% +
    'doc_pay_date',  # 70% +
    # 'doc_total',
    # # CS
    'supplier_org',  # 70%+
    'customer_org',  # 70%+
    'customer_postal',
    'supplier_postal',
    # 'customer_city',
    # 'supplier_city',

    # 'supplier_contact',
    # 'doc_customer_ref',
    #'supplier_country_short',
    #'customer_country_short'
]

FIELD2CLF = {
    'doc_pay_iban': DocPayIban,
    'doc_date': DocDate,
    'doc_pay_date': DocPayDate,
    'doc_total': DocTotal,
    'doc_number': DocNumber,
    'supplier_org': SupplierOrg,
    'customer_org': CustomerOrg,
    'supplier_postal': SupplierPostal,
    'customer_postal': CustomerPostal,
    'supplier_city': SupplierCity,
    'customer_city': CustomerCity,
    'supplier_contact': SupplierContact,
    'doc_customer_ref': DocCustomerRef,
}

ALL_FIELDS = [
    'doc_number',
    'doc_date',
    'doc_delivery_date',
    'doc_order_ref',
    'doc_customer_ref',
    'doc_currency',
    'doc_note',
    'supplier_org',
    'supplier_name',
    'supplier_street',
    'supplier_postal',
    'supplier_city',
    'supplier_country_short',
    'supplier_contact',
    'customer_org',
    'customer_name',
    'customer_street',
    'customer_postal',
    'customer_city',
    'customer_country_short',
    'doc_pay_date',
    'doc_pay_id',
    'doc_pay_method',
    'doc_pay_bban',
    'doc_pay_iban',
    'doc_pay_bic',
    'doc_total',
    'doc_total_vat_ex',
    'doc_rounding',
    'doc_total_vat_in'
]