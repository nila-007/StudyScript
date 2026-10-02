# lexer.py

# -----------------------------
# Token Class
# -----------------------------

class Token:
    def __init__(self, token_type, value, line, column):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.column})"


# -----------------------------
# Lexer Class
# -----------------------------

class Lexer:

    # Keywords in StudyScript
    KEYWORDS = {
        "SET": "SET",
        "STUDY": "STUDY",
        "BREAK": "BREAK",
        "FOR": "FOR",
        "IF": "IF",
        "END": "END",
        "REPEAT": "REPEAT"
    }

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    # -----------------------------
    # Current Character
    # -----------------------------

    def current_char(self):
        if self.position >= len(self.source):
            return None

        return self.source[self.position]

    # -----------------------------
    # Move to Next Character
    # -----------------------------

    def advance(self):
        if self.position >= len(self.source):
            return

        if self.source[self.position] == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.position += 1

    # -----------------------------
    # Skip Spaces and New Lines
    # -----------------------------

    def skip_whitespace(self):
        while self.current_char() is not None and self.current_char().isspace():
            self.advance()

    # -----------------------------
    # Read Number
    # -----------------------------

    def read_number(self):
        start_column = self.column
        number = ""

        while self.current_char() is not None and self.current_char().isdigit():
            number += self.current_char()
            self.advance()

        return Token(
            "NUMBER",
            number,
            self.line,
            start_column
        )

    # -----------------------------
    # Read Identifier / Keyword
    # -----------------------------

    def read_identifier(self):
        start_column = self.column
        word = ""

        while (
            self.current_char() is not None
            and (
                self.current_char().isalnum()
                or self.current_char() == "_"
            )
        ):
            word += self.current_char()
            self.advance()

        # Check whether it is a keyword
        if word.upper() in self.KEYWORDS:
            token_type = self.KEYWORDS[word.upper()]
        else:
            token_type = "IDENTIFIER"

        return Token(
            token_type,
            word,
            self.line,
            start_column
        )

    # -----------------------------
    # Read String
    # -----------------------------

    def read_string(self):
        start_column = self.column

        # Skip opening quote
        self.advance()

        value = ""

        while self.current_char() is not None and self.current_char() != '"':
            value += self.current_char()
            self.advance()

        # Missing closing quote
        if self.current_char() is None:
            raise Exception(
                f"Lexical Error: Unterminated string at line {self.line}"
            )

        # Skip closing quote
        self.advance()

        return Token(
            "STRING",
            value,
            self.line,
            start_column
        )

    # -----------------------------
    # Main Tokenization Function
    # -----------------------------

    def tokenize(self):

        while self.current_char() is not None:

            char = self.current_char()

            # Ignore spaces
            if char.isspace():
                self.skip_whitespace()
                continue

            # Number
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue

            # Identifier / Keyword
            if char.isalpha() or char == "_":
                self.tokens.append(self.read_identifier())
                continue

            # String
            if char == '"':
                self.tokens.append(self.read_string())
                continue

            # -------------------------
            # Single-character operators
            # -------------------------

            if char == "+":
                self.tokens.append(
                    Token("PLUS", char, self.line, self.column)
                )
                self.advance()
                continue

            if char == "-":
                self.tokens.append(
                    Token("MINUS", char, self.line, self.column)
                )
                self.advance()
                continue

            if char == "*":
                self.tokens.append(
                    Token("MULTIPLY", char, self.line, self.column)
                )
                self.advance()
                continue

            if char == "/":
                self.tokens.append(
                    Token("DIVIDE", char, self.line, self.column)
                )
                self.advance()
                continue

            if char == "=":
                # Check for ==
                if self.position + 1 < len(self.source) and self.source[self.position + 1] == "=":
                    self.tokens.append(
                        Token("EQUAL", "==", self.line, self.column)
                    )
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(
                        Token("ASSIGN", "=", self.line, self.column)
                    )
                    self.advance()

                continue

            if char == ">":
                # Check for >=
                if self.position + 1 < len(self.source) and self.source[self.position + 1] == "=":
                    self.tokens.append(
                        Token("GREATER_EQUAL", ">=", self.line, self.column)
                    )
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(
                        Token("GREATER", ">", self.line, self.column)
                    )
                    self.advance()

                continue

            if char == "<":
                # Check for <=
                if self.position + 1 < len(self.source) and self.source[self.position + 1] == "=":
                    self.tokens.append(
                        Token("LESS_EQUAL", "<=", self.line, self.column)
                    )
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(
                        Token("LESS", "<", self.line, self.column)
                    )
                    self.advance()

                continue

            if char == "!":
                # Only != is allowed
                if self.position + 1 < len(self.source) and self.source[self.position + 1] == "=":
                    self.tokens.append(
                        Token("NOT_EQUAL", "!=", self.line, self.column)
                    )
                    self.advance()
                    self.advance()
                    continue
                else:
                    raise Exception(
                        f"Lexical Error: Invalid character '!' "
                        f"at line {self.line}, column {self.column}"
                    )

            # Parentheses
            if char == "(":
                self.tokens.append(
                    Token("LPAREN", char, self.line, self.column)
                )
                self.advance()
                continue

            if char == ")":
                self.tokens.append(
                    Token("RPAREN", char, self.line, self.column)
                )
                self.advance()
                continue

            # -------------------------
            # Invalid Character
            # -------------------------

            raise Exception(
                f"Lexical Error: Invalid character '{char}' "
                f"at line {self.line}, column {self.column}"
            )

        # End of file
        self.tokens.append(
            Token("EOF", "", self.line, self.column)
        )

        return self.tokens