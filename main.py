from lexer import Lexer
from parser import Parser


source = """
SET HOURS = 5

IF HOURS > 4
    STUDY "Compiler Design" FOR 2 HOURS
END
"""


# -----------------------------
# Lexical Analysis
# -----------------------------

lexer = Lexer(source)

tokens = lexer.tokenize()

print("========== TOKENS ==========")

for token in tokens:
    print(token)


# -----------------------------
# Syntax Analysis
# -----------------------------

parser = Parser(tokens)

ast = parser.parse()

print("\n========== AST ==========")

print(ast)