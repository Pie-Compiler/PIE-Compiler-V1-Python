class PLYLexerAdapter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.lineno = 1
        self.lexpos = 0
        
    def token(self):
        if self.pos >= len(self.tokens):
            return None
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok