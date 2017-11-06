from helpers.xml_helper import extract_pdf_from_xml
import os, glob
from settings import *


for xml_path in glob.glob(HOME_DIR + os.sep + 'data2' + os.sep + '*.xml'):
    extract_pdf_from_xml(xml_path)