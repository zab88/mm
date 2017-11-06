from src.clf.GeneralClf import GeneralClf


class CSContact(GeneralClf):
    # SQL_FIELD = ['supplier_contact', 'doc_customer_ref']

    @staticmethod
    def is_candidate(s):
        if len(s) < 2:
            return False
        if any(x.isdigit() for x in s):
            return False
        # if not any(x.isdigit() for x in s):
        #     return False
        if not s[0].isupper():
            return False
        if len([x for x in s if x.isupper()]) not in [2, 3]:
            return False
        name_str = s[0]
        for k, x in enumerate(s):
            if k == 0:
                continue
            if x.isupper():
                name_str = name_str + ' ' + x
            else:
                name_str += x
        s_cleaned = ''.join([x.upper() if x.isalpha() or x == ' ' else '' for x in name_str])
        for chunk in s_cleaned.split():
            if len(chunk) < 3:
                return False
        return s_cleaned

    @staticmethod
    def is_valid(s):
        return True
