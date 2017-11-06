import glob, os
from helpers.xml_helper import read_xml_model
from settings import *


def only_alpha(s):
    return ''.join([x if x.isalpha() else '' for x in s])


def search_title(title, model):
    found_tokens = []
    avg_height = []
    for token in model.tokens:
        avg_height.append(token.h)
        if token.txt.upper() == title.upper():
            found_tokens.append(token)
    if len(found_tokens) == 0:
        return False
    if len(found_tokens) > 0:
        return True
    # print(found_tokens)
    # checking for space around and height
    avg_height = sum(avg_height)/len(avg_height)
    for token in found_tokens:
        if token.h <= avg_height:
            continue
        if token.h > avg_height:
            return True
        x_spasing, y_spasing = token.h, token.h/2
        tokens_y = [t for t in model.tokens if t.y+t.h+y_spasing > token.y and token.y+token.h+y_spasing > t.y]
        tokens_xy = [t for t in tokens_y if t.x+t.w+x_spasing > token.x and token.x+token.w+x_spasing > t.x]
        # only same token
        if len(tokens_xy) == 1:
            return True
    return False

features_X, answers_Y, bad_docs = [], [], []
detected_invoices = []
for xml_path in glob.glob(HOME_DIR + '/data_test/xml_models/*.xml'):  # 812160842_0000676862_Faktura_175722
    model = read_xml_model(xml_path)
    if len(model.tokens) < 1:
        bad_docs.append(xml_path)
        continue
    abn_file = os.path.basename(xml_path).replace('..xml', '.abn')
    # print(abn_file)
    is_attachment = True if os.path.isfile(HOME_DIR + '/Testdata/{}'.format(abn_file)) else False

    is_invoice_title = search_title('FAKTURA', model)
    if is_invoice_title:
        detected_invoices.append(xml_path)

    if is_attachment and is_invoice_title:
        print('ERROR', xml_path)

print('Total invoices with title: ', len(detected_invoices))
for ii in detected_invoices:
    print(ii)

    # extract features
    # txt = ' '.join([only_alpha(x.txt) for x in model.tokens])

    # features_X.append(txt)
    # answers_Y.append(is_attachment)


