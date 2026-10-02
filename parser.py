# parser.py

from ast import (
    Program,
    SetStatement,
    StudyStatement,
    BreakStatement,
    IfStatement,
    RepeatStatement,
    BinaryExpression,
    NumberLiteral,
    StringLiteral,
    Identifier
)


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    # ==========================================
    # Current Token
    # ==========================================

    def current_token(self):
        return self.tokens[self.position]

    # ==========================================
    # Move to Next Token
    # ==========================================

    def advance(self):
        if self.position < len(self.tokens) - 1:
            self.position += 1

    # ==========================================
    # Check Token Type
    # ==========================================

    def check(self, token_type):
        return self.current_token().type == token_type

    # ==========================================
    # Expect Token
    # ==========================================

    def expect(self, token_type):
        token = self.current_token()

        if token.type != token_type:
            raise Exception(
                f"Syntax Error: Expected {token_type}, "
                f"but found {token.type} "
                f"at line {token.line}, column {token.column}"
            )

        self.advance()
        return token

    # ==========================================
    # Parse Entire Program
    # ==========================================

    def parse(self):

        statements = []

        while not self.check("EOF"):

            statement = self.parse_statement()

            statements.append(statement)

        return Program(statements)

    # ==========================================
    # Parse Statement
    # ==========================================

    def parse_statement(self):

        if self.check("SET"):
            return self.parse_set()

        if self.check("STUDY"):
            return self.parse_study()

        if self.check("BREAK"):
            return self.parse_break()

        if self.check("IF"):
            return self.parse_if()

        if self.check("REPEAT"):
            return self.parse_repeat()

        token = self.current_token()

        raise Exception(
            f"Syntax Error: Unexpected token "
            f"{token.type} at line {token.line}"
        )

    # ==========================================
    # SET statement
    # ==========================================

    def parse_set(self):

        self.expect("SET")

        variable = self.expect("IDENTIFIER")

        self.expect("ASSIGN")

        expression = self.parse_expression()

        return SetStatement(
            Identifier(variable.value),
            expression
        )

    # ==========================================
    # STUDY statement
    # ==========================================

    def parse_study(self):

        self.expect("STUDY")

        subject = self.expect("STRING")

        self.expect("FOR")

        duration = self.parse_expression()

        if self.check("IDENTIFIER") and self.current_token().value.upper() == "HOURS":unit = self.expect("IDENTIFIER")
        elif self.check("IDENTIFIER") and self.current_token().value.upper() == "MINUTES":unit = self.expect("IDENTIFIER")
        else:
            token = self.current_token()

            raise Exception(
              f"Syntax Error: Expected HOURS or MINUTES "
              f"at line {token.line}"
            )

        return StudyStatement(
            StringLiteral(subject.value),
            duration,
            unit.value
        )

    # ==========================================
    # BREAK statement
    # ==========================================

    def parse_break(self):

        self.expect("BREAK")

        self.expect("FOR")

        duration = self.parse_expression()

        if self.check("IDENTIFIER") and self.current_token().value.upper() == "HOURS":unit = self.expect("IDENTIFIER")
        elif self.check("IDENTIFIER") and self.current_token().value.upper() == "MINUTES":unit = self.expect("IDENTIFIER")
        else:
            token = self.current_token()

            raise Exception(
                f"Syntax Error: Expected HOURS or MINUTES "
                f"at line {token.line}"
            )

        return BreakStatement(
            duration,
            unit.value
        )

    # ==========================================
    # IF statement
    # ==========================================

    def parse_if(self):

        self.expect("IF")

        condition = self.parse_expression()

        body = []

        while not self.check("END") and not self.check("EOF"):
            body.append(self.parse_statement())

        self.expect("END")

        return IfStatement(
            condition,
            body
        )

    # ==========================================
    # REPEAT statement
    # ==========================================

    def parse_repeat(self):

        self.expect("REPEAT")

        count = self.parse_expression()

        body = []

        while not self.check("END") and not self.check("EOF"):
            body.append(self.parse_statement())

        self.expect("END")

        return RepeatStatement(
            count,
            body
        )

    # ==========================================
    # Expression
    # ==========================================

    def parse_expression(self):

        return self.parse_comparison()

    # ==========================================
    # Comparison
    # ==========================================

    def parse_comparison(self):

        left = self.parse_term()

        comparison_operators = [
            "GREATER",
            "LESS",
            "GREATER_EQUAL",
            "LESS_EQUAL",
            "EQUAL",
            "NOT_EQUAL"
        ]

        while self.current_token().type in comparison_operators:

            operator = self.current_token().value

            self.advance()

            right = self.parse_term()

            left = BinaryExpression(
                left,
                operator,
                right
            )

        return left

    # ==========================================
    # Addition / Subtraction
    # ==========================================

    def parse_term(self):

        left = self.parse_factor()

        while self.check("PLUS") or self.check("MINUS"):

            operator = self.current_token().value

            self.advance()

            right = self.parse_factor()

            left = BinaryExpression(
                left,
                operator,
                right
            )

        return left

    # ==========================================
    # Multiplication / Division
    # ==========================================

    def parse_factor(self):

        left = self.parse_primary()

        while self.check("MULTIPLY") or self.check("DIVIDE"):

            operator = self.current_token().value

            self.advance()

            right = self.parse_primary()

            left = BinaryExpression(
                left,
                operator,
                right
            )

        return left

    # ==========================================
    # Primary Expressions
    # ==========================================

    def parse_primary(self):

        token = self.current_token()

        # Number
        if token.type == "NUMBER":

            self.advance()

            return NumberLiteral(token.value)

        # Identifier
        if token.type == "IDENTIFIER":

            self.advance()

            return Identifier(token.value)

        # Parentheses
        if token.type == "LPAREN":

            self.advance()

            expression = self.parse_expression()

            self.expect("RPAREN")

            return expression

        raise Exception(
            f"Syntax Error: Unexpected token "
            f"{token.type} at line {token.line}"
        )