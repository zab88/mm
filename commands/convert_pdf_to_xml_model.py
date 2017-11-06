from helpers.pdf_helper import pdf_to_png
from helpers.pdf_helper import img_to_xytext
from helpers.xml_helper import write_xml_model, read_xml_model
import glob, os, cv2
from settings import *
from stdnum import iban, iso9362


for pdf_path in glob.glob(HOME_DIR + os.sep + 'Testdata' + os.sep + '*.pdf'):
    # 1. convert to img
    if os.path.isfile(HOME_DIR + os.sep + 'data_test/images_tmp' + os.sep + os.path.basename(pdf_path).replace('.pdf', '-1.png')):
        print('already converted')
        continue

    img_paths, errors = pdf_to_png(pdf_path, HOME_DIR + os.sep + 'data_test' + os.sep + 'images_tmp' + os.sep)
    # 2. process with tesseract
    tokens = []
    for page, img_path in enumerate(img_paths):
        l, err = img_to_xytext(img_path, HOME_DIR + os.sep + 'data_test' + os.sep + 'tsv_tmp' + os.sep, page=page+1)
        tokens += l
    # 3. write xml model
    write_xml_model(tokens, file_name=HOME_DIR + '/data_test/xml_models/' + os.path.basename(pdf_path)[:-3] + '.xml')
    print(tokens)
    # exit()
