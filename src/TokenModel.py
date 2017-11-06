class TokenModel:
    MAX_VALUABLE_DISTANCE = 1200

    def __init__(self, token_dict):
        self.txt = token_dict['txt']

        self.x = int(token_dict['x'])
        self.y = int(token_dict['y'])
        self.w = int(token_dict['w'])
        self.h = int(token_dict['h'])

        self.page_num = token_dict['page_num']
        self.line_num = token_dict['line_num']
        self.block_num = token_dict['block_num']

    def __sub__(self, other):
        if len([x for x in other.txt if x.isalpha()]) < 2:
            return 2480+3509
        if abs(self.x - other.x) > 100 and abs(self.y - other.y) > 100:
            return 2480 + 3509
        # d = abs(self.x - other.x)**2 + abs(self.y - other.y)**2
        d = abs(self.x - other.x) + abs(self.y - other.y)
        # if self.x - other.x < 0:
        #     d *= -1
        return d

    @staticmethod
    def get_upper_tokens(token, other_tokens):
        thres1, thres2 = 100, 100
        # upper_tokens = [t for t in other_tokens if t.y < token.y < t.y - 200 and t.page_num == token.page_num]
        upper_tokens = [t for t in other_tokens if t.y < token.y < t.y + 200 and t.page_num == token.page_num]
        upper_tokens = [t for t in upper_tokens if t.x - thres1 < token.x < t.x + thres2]
        upper_tokens = sorted(upper_tokens, key=lambda t: t.y)[-2:]
        return upper_tokens
