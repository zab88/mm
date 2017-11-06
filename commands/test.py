"""
usage: python3 test.py <path_to_invoice_pdf>
"""
from helpers.pdf_helper import pdf_to_png
from helpers.pdf_helper import img_to_xytext
from helpers.xml_helper import write_xml_model, read_xml_model
from sklearn.externals import joblib
import glob, os, sys
import cv2
from settings import *


TO_DRAW = True
if len(sys.argv) < 2:
    print(__doc__)
    exit()
else:
    pdf_path = sys.argv[1]
    # check if file exists
    if not os.path.isfile(pdf_path):
        print('Invalid path to pdf file {}'.format(os.path.abspath(pdf_path)))
        exit()

    # making xml, we are using tmp directory
    img_paths, errors = pdf_to_png(pdf_path, HOME_DIR + os.sep + 'tmp' + os.sep)
    tokens = []
    for page, img_path in enumerate(img_paths):
        l, err = img_to_xytext(img_path, HOME_DIR + os.sep + 'tmp' + os.sep, page=page + 1)
        tokens += l
    # write xml model
    write_xml_model(tokens, file_name=HOME_DIR + '/tmp/' + os.path.basename(pdf_path)[:-4] + '.xml')

    text_model = read_xml_model(HOME_DIR + '/tmp/' + os.path.basename(pdf_path)[:-4] + '.xml')
    # text_model = read_xml_model(r'C:\MyPrograms\python3\invoiceai/tmp/5659287_31585865966058bdaa86_ehf.xml')
    # Now model created

    # for each classifier getting predicted values
    predicted_list = []
    for field_name in IMPLEMENTED_FIELDS:
        # reading saved pkl
        clf_class = joblib.load(HOME_DIR + os.sep + 'trained_classes' + os.sep + field_name + '.pkl')
        # clf_class_name = FIELD2CLF[field_name]
        # clf_class = clf_class_name()

        predicted = clf_class.predict_invoice(text_model)
        if predicted is None:
            predicted_cleaned = None
        else:
            predicted_cleaned = predicted[2]
            predicted_list.append(predicted[:])

        print("{} is {}".format(field_name, predicted_cleaned))

    if TO_DRAW:
        img_origin = cv2.imread(img_paths[0])
        for wm in predicted_list:
            if int(wm[1].tokens[0].page_num) != 1:
                continue
            offset_1, offset_2 = wm[4][0], wm[4][0]+wm[4][0]+1
            x = min([x.x for x in wm[1].tokens[offset_1:offset_2]])
            y = min([x.y for x in wm[1].tokens[offset_1:offset_2]])
            w = max([x.x + x.w for x in wm[1].tokens[offset_1:offset_2]]) - x
            h = max([x.y + x.h for x in wm[1].tokens[offset_1:offset_2]]) - y
            cv2.rectangle(img_origin, (x, y), (x+w, y+h), (30, 30, 220), 2)

        cv2.imshow('res', cv2.pyrDown(img_origin))
        cv2.imwrite(HOME_DIR + '/tmp/HL-' + os.path.basename(pdf_path)[:-4] + '-HL.png', img_origin)
        cv2.waitKey()
