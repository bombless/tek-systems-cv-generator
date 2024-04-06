class Parser:
    def __init__(self, input):
        self.tokens = TokenParser(input)
        self.buffer = []
        self.offset = 0

    def next_token(self):
        if self.offset >= len(self.buffer):
            self.buffer.append(self.tokens.next())
        ret = self.buffer[self.offset]
        self.offset += 1
        return ret

    def swallow(self, t):
        if self.buffer[self.offset - 1] != t:
            raise Exception('wrong value')
        self.offset -= 1

    def peek(self):
        t = self.next_token()
        self.swallow(t)
        return t

    def save(self):
        return self.offset

    def load(self, offset):
        self.offset = offset

    def parse_entry(self):
        curr = self.next_token()
        if curr is None:
            return False, None
        if curr.is_entry():
            return True, curr
        self.swallow(curr)
        return False, None

    def parse_comma(self):
        curr = self.next_token()
        if curr.is_comma():
            return True, curr
        self.swallow(curr)
        return False,

    def parse_left_paren(self):
        curr = self.next_token()
        if curr.is_left_paren():
            return True, curr
        self.swallow(curr)
        return False

    def parse_right_paren(self):
        curr = self.next_token()
        if curr.is_right_paren():
            return True, curr
        self.swallow(curr)
        return False

    def parse_string(self):
        curr = self.next_token()
        if curr.is_string():
            return True, curr
        self.swallow(curr)
        return False,

    def parse_item(self):
        checkpoint = self.save()
        ok, _ = self.parse_entry()
        if not ok:
            return False, None
        ok, _ = self.parse_left_paren()
        if not ok:
            self.load(checkpoint)
            return False, None

        content = []
        while True:
            p = self.peek()
            if p.is_right_paren():
                self.next_token()
                return True, content
            if p.is_string():
                content.append(p.get_content())
                self.next_token()
                p = self.peek()
                if p.is_comma():
                    self.next_token()
                elif not p.is_right_paren() and not p.is_string():
                    self.load(checkpoint)
                    return False,


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

    def get_content(self):
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

    def __repr__(self):
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

            raise Exception("unknown character " + c + " index " + str(advance))
