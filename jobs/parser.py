class Parser:
    def __init__(self):
        self.entries = []


class Token:
    def __init__(self, typ, cnt=None):
        self.type = typ
        self.content = cnt

    def is_left_paren(self):
        return self.type == 'lp'

    def is_right_paren(self):
        return self.type == 'rp'

    def is_string(self):
        return self.type == 's'

    def content(self):
        return self.content

    def is_comma(self):
        return self.type == 'c'

    def is_entry(self):
        return self.type == 'e'

    @staticmethod
    def lp():
        return Token('lp')

    @staticmethod
    def rp():
        return Token('rp')

    @staticmethod
    def s(c):
        return Token('s', c)

    @staticmethod
    def c():
        return Token('c')

    @staticmethod
    def e():
        return Token('e')

    def __str__(self):
        return self.type


class TokenParser:
    def __init__(self, input):
        self.input = input

    def peek(self, n=0):
        return self.input[n]

    def peek_n(self, n, length):
        return self.input[n:n + length] if len(self.input) > n + length else self.input[n]

    def advance(self, n=1):
        self.input = self.input[n:]

    def next(self):
        if len(self.input) == 0:
            return None
        in_string_literal = False
        str_content = ''
        c = self.peek()
        advance = 1
        peek = 0
        while True:

            if in_string_literal:
                if c == '"':
                    self.advance(advance)
                    return Token.s(str_content)
                str_content += c
                c = self.peek(advance)
                advance += 1
                continue
            elif c == '"':
                in_string_literal = True
                c = self.peek(advance)
                advance += 1
                continue

            if c.isspace():
                c = self.peek(advance)
                advance += 1
                peek += 1
                continue
            if c == '(':
                self.advance(advance)
                return Token.lp()
            if c == ')':
                self.advance(advance)
                return Token.rp()
            if c == ',':
                self.advance(advance)
                return Token.c()

            if self.peek_n(peek, 5) == "entry":
                advance += 4
                self.advance(advance)
                return Token.e()

            raise Exception("unknown character " + c + " index " + str(advance) + " input " + self.input)
