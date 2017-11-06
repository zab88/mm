from settings import *
from helpers.db_helper import get_correct_values, get_values_iban
from helpers.xml_helper import read_xml_model
from src.clf.GeneralClf import GeneralClf


def get_docs_4_train(field):
    db_values = get_correct_values([field])
    models = []
    fields = []

    for f_name in db_values:
        # some limit can be set for debug
        # if len(fields) > 100:
        #     break

        # model = read_xml_model(xml_path)
        model = read_xml_model(HOME_DIR + '/data_test/xml_models/' + f_name['file_name'].replace(".xml", "..xml"))
        model.setFileName(f_name['file_name'])
        if len(model.words) > 0 and f_name[field]:
            models.append(model)
            fields.append(f_name[field])
    return models, fields


def make_matrix(clf_class, models, fields):
    features_X = []
    answers_Y = []

    for k, model in enumerate(models):
        candidates = clf_class.get_candidates(model)

        found = False
        if len(candidates):
            # print(candidates)
            for candidate in candidates:
                # print(candidate[2].encode('utf-8'), '---', fields[k].encode('utf-8'), '+++', (candidate[2] == fields[k]))
                # if candidate[2] == fields[k]:
                # if fields[k] == '123,52':
                #     print(candidate[2])
                if GeneralClf.compare(candidate[2], fields[k], candidate[3]):
                    # print(f_name[field] + ' is candidate')
                    # features_X.append(GeneralClf.get_features(candidate[1]))
                    features_X.append(GeneralClf.get_features_advanced(model, candidate))
                    answers_Y.append(1)
                    found = True
                else:
                    # features_X.append(GeneralClf.get_features(candidate[1]))
                    features_X.append(GeneralClf.get_features_advanced(model, candidate))
                    answers_Y.append(0)
        # if not found:
        #     print('NO CANDIDATE: {} "{}"'.format(model.file_name, fields[k]))
    return features_X, answers_Y


# return array of features and answers
def get_XY(field):
    if field == 'doc_pay_iban':
        db_values = get_values_iban()
    else:
        db_values = get_correct_values([field])
    # for x in db_values:
    #     print(x)

    models = []
    features_X = []
    answers_Y = []
    documents_Z = []

    found_num, processed_num = 0, 0
    # for xml_path in glob.glob(HOME_DIR + os.sep + 'data_test' + os.sep + 'xml_models' + os.sep + '*.xml'):
    for f_name in db_values:
        processed_num += 1
        # some limit can be set for debug
        # if found_num > 20:
        #     break

        # model = read_xml_model(xml_path)
        model = read_xml_model(HOME_DIR + '/data_test/xml_models/' + f_name['file_name'].replace(".xml", "..xml"))
        models.append(model)
        clf_class = FIELD2CLF[field]
        candidates = clf_class.get_candidates(model)

        if len(candidates):
            # print(candidates)
            found_num += 1
            for candidate in candidates:
                # print(candidate[2], '---', f_name[field], '+++')
                if candidate[2] == f_name[field]:
                    # print(f_name[field] + ' is candidate')
                    features_X.append(GeneralClf.get_features(candidate[1]))
                    answers_Y.append(1)
                    documents_Z.append(f_name['file_name'].replace('.xml', ''))
                else:
                    features_X.append(GeneralClf.get_features(candidate[1]))
                    answers_Y.append(0)
                    documents_Z.append(f_name['file_name'].replace('.xml', ''))
                    # print('NOT!')
        else:
            if not DEBUG:
                print(f_name)
        # exit()

    return features_X, answers_Y, documents_Z, found_num, processed_num
