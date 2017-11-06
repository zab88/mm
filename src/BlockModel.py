class BlockModel:
    def __init__(self, tokens):
        self.txt = []
        self.tokens = tokens[:]
        self.block_num = self.tokens[0].block_num
        for token in tokens:
            self.txt.append(token.txt)
        self.txt = ' '.join(self.txt)
