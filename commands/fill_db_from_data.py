"""
This command:
1. goes through xml files in invoice data set (directory "data2")
2. extracts fields we need from xml, according to https://docs.google.com/document/d/1sIRctMDonu0RvE1tenPZoC09-LFiMRJXHAK4qB4YwYA/edit
3. fill DB with data from xml. DB structure defined at helpers/invvoiceai.sql
"""
from helpers.xml_helper import get_invoice_fields
from helpers.db_helper import fill_db
import glob, os
from settings import *


for path_to_xml in glob.glob(HOME_DIR + os.sep + 'data2' + os.sep + '*.xml'):
    print(path_to_xml)
    fields = get_invoice_fields(path_to_xml)
    print(fields)
    fill_db(fields_dict=fields, file_name=os.path.basename(path_to_xml))
    # exit()
