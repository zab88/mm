class WordModel:
    def __init__(self, tokens):
        self.txt = []
        self.tokens = tokens[:]
        for token in tokens:
            self.txt.append(token.txt)
        self.txt = ' '.join(self.txt)
