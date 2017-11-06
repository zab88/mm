from bs4 import BeautifulSoup
import os
import copy
from src.TokenModel import TokenModel
from src.InvoiceModel import InvoiceModel
import base64


# UBL 2.1 format
def get_invoice_fields(path_to_xml):
    xml_handler = open(path_to_xml, encoding='utf-8').read()
    soup = BeautifulSoup(xml_handler, 'xml')

    # document fields. Include name and path through tags in xml
    fields_dict = {
                   'doc_number': ['ID'],
                   'doc_date': ['IssueDate'],
                   'doc_delivery_date': ['Delivery', 'ActualDeliveryDate'],
                   'doc_order_ref': ['OrderReference', 'ID'],
                   'doc_customer_ref': ['AccountingCustomerParty', 'Party', 'Contact', 'ID'],
                   # 'doc_account_number': ['ProfileID'], #
                   'doc_currency': ['DocumentCurrencyCode'],
                   'doc_note': ['Note'],

                   'doc_total_vat_in': ['LegalMonetaryTotal', 'PayableAmount'],
                   'doc_total_vat_ex': ['LegalMonetaryTotal', 'TaxExclusiveAmount'],
                   'doc_rounding': ['LegalMonetaryTotal', 'PayableRoundingAmount'],
                   'doc_total': ['LegalMonetaryTotal', 'LineExtensionAmount'],

                   # 'doc_discount': [],  # ?
                   # 'doc_subtotal': ['TaxTotal', 'TaxSubtotal', 'TaxableAmount'],
                   # 'doc_tax': ['TaxTotal', 'TaxAmount'],
                   # 'doc_total_usd': [],  # ?

                   'doc_pay_date': ['PaymentMeans', 'PaymentDueDate'],
                   'doc_pay_id': ['PaymentMeans', 'PaymentID'],
                   'doc_pay_method': ['PaymentMeans', 'PaymentMeansCode'],
                   'doc_pay_bic': ['PaymentMeans', 'PayeeFinancialAccount', 'FinancialInstitutionBranch', 'FinancialInstitution', 'ID'],
                   # 'doc_pay_swift': [],  # probably can be extracted from iban bban
                   'doc_pay_bban': ['PaymentMeans', 'PayeeFinancialAccount', 'ID'],
                   'doc_pay_iban': ['PaymentMeans', 'PayeeFinancialAccount', 'ID'],

                   'supplier_org': ['AccountingSupplierParty', 'Party', 'PartyLegalEntity', 'CompanyID'],
                   'supplier_name': ['AccountingSupplierParty', 'Party', 'PartyName', 'Name'],
                   # 'supplier_org': ['AccountingSupplierParty', 'Party', 'PartyIdentification', 'ID'],
                   # 'supplier_cvr': [],  # ?
                   # 'supplier_gln': [],  # ?
                   'supplier_country_short': ['AccountingSupplierParty', 'Party', 'PostalAddress', 'Country', 'IdentificationCode'],
                   'supplier_city': ['AccountingSupplierParty', 'Party', 'PostalAddress', 'CityName'],
                   'supplier_street': ['AccountingSupplierParty', 'Party', 'PostalAddress', 'StreetName'],
                   'supplier_postal': ['AccountingSupplierParty', 'Party', 'PostalAddress', 'PostalZone'],
                   'supplier_contact': ['AccountingSupplierParty', 'Party', 'Contact', 'ID'],
                   # 'supplier_zip': [],  # probably can extracted from postal and address
                   # 'supplier_phone': [],  # ?
                   # 'supplier_email': [],  # ?

                   'customer_org': ['AccountingCustomerParty', 'Party', 'PartyLegalEntity', 'CompanyID'],
                   'customer_name': ['AccountingCustomerParty', 'Party', 'PartyName', 'Name'],
                   # 'customer_cvr': [],  # ?
                   # 'customer_gln': [],  # ?
                   'customer_country_short': ['AccountingCustomerParty', 'Party', 'PostalAddress', 'Country', 'IdentificationCode'],
                   'customer_city': ['AccountingCustomerParty', 'Party', 'PostalAddress', 'CityName'],
                   'customer_street': ['AccountingCustomerParty', 'Party', 'PostalAddress', 'StreetName'],
                   'customer_postal': ['AccountingCustomerParty', 'Party', 'PostalAddress', 'PostalZone'],
                   # 'customer_zip': [],  # probably can extracted from postal and address
                   # 'customer_phone': [],  # ?
                   # 'customer_email': [],  # ?

                   # 's_vat': ['AccountingSupplierParty', 'Party', 'PartyIdentification', 'ID'],
                   # 'c_vat': ['AccountingCustomerParty', 'Party', 'PartyTaxScheme', 'CompanyID'],
                  }
    res_dict = {}

    # reading
    for response_name in fields_dict:
        current_tag = copy.copy(soup)
        for tag in fields_dict[response_name]:
            current_tag = current_tag.find(tag)
            if current_tag is None:
                break
        if current_tag is None or len(fields_dict[response_name]) == 0:
            res = None
        else:
            res = current_tag.get_text().strip()  # strip deletes new lines in company names
        # print(response_name, res)
        res_dict[response_name] = res

    return res_dict


def write_xml_model(tokens, file_name):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<xml_model>\n'

    for token in tokens:
        s = []
        xml += '<text '
        txt = ''
        for name, value in token.items():
            if name == 'txt':
                txt = value[:]
                continue
            s.append(str(name) + '="' + str(value) + '"')
        xml += ' '.join(s)
        xml += '>'+ txt + '</text>\n'

    xml += '</xml_model>'
    file = open(file_name, 'w', encoding='utf-8')
    file.write(xml)
    file.close()


def read_xml_model(model_path):
    xml_handler = open(model_path, encoding='utf-8').read()
    soup = BeautifulSoup(xml_handler, 'xml')

    tokens = []
    for el in soup.find_all('text'):
        d = {
            'x': el.get('x'),
            'y': el.get('y'),
            'w': el.get('w'),
            'h': el.get('h'),
            'txt': el.get_text(),
            'page_num': el.get('page_num'),
            'line_num': el.get('line_num'),
            'block_num': el.get('block_num')
        }
        token = TokenModel(d)
        tokens.append(token)
    model = InvoiceModel(tokens=tokens)
    return model


def extract_pdf_from_xml(xml_path):
    xml_handler = open(xml_path, encoding='utf-8').read()
    soup = BeautifulSoup(xml_handler, 'xml')

    pdf_text = soup.find('EmbeddedDocumentBinaryObject').get_text()
    pdf_bin = base64.decodebytes(pdf_text.encode('ascii'))  # utf8

    pdf_file = open(xml_path[:-3] + 'pdf', 'wb')
    pdf_file.write(pdf_bin)
    pdf_file.close()
