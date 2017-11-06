from src.WordModel import WordModel
from src.BlockModel import BlockModel
from itertools import groupby


class InvoiceModel:
    def __init__(self, tokens):
        self.tokens = tokens

        self.tokens = tokens[:]
        self.words = []
        self.blocks = []
        self.tokens = sorted(self.tokens, key=lambda x: x.block_num)
        self.file_name = None
        current_block = -1
        current_line = -1
        current_tokens = []
        for token in self.tokens:
            # new block started
            if token.block_num != current_block or token.line_num != current_line:
                # if we have something in block
                if len(current_tokens) > 0:
                    self.words.append(WordModel(current_tokens))
                    current_tokens = []
                current_block = token.block_num
                current_line = token.line_num
                current_tokens.append(token)
            else:
                current_tokens.append(token)
        # finally
        if len(current_tokens) > 0:
            self.words.append(WordModel(current_tokens))

        # filling blocks
        block_lambda = lambda x: x.block_num
        block_lists = [list(g[1]) for g in groupby(self.tokens, block_lambda)]
        for block_list in block_lists:
            self.blocks.append(BlockModel(block_list))

    def setFileName(self, file_name):
        self.file_name = file_name
