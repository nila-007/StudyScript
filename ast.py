# ast.py

# ==========================================
# Base AST Node
# ==========================================

class ASTNode:
    pass


# ==========================================
# Program
# ==========================================

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"


# ==========================================
# Statements
# ==========================================

class SetStatement(ASTNode):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def __repr__(self):
        return (
            f"SetStatement("
            f"variable={self.variable}, "
            f"expression={self.expression})"
        )


class StudyStatement(ASTNode):
    def __init__(self, subject, duration, unit):
        self.subject = subject
        self.duration = duration
        self.unit = unit

    def __repr__(self):
        return (
            f"StudyStatement("
            f"subject={self.subject}, "
            f"duration={self.duration}, "
            f"unit={self.unit})"
        )


class BreakStatement(ASTNode):
    def __init__(self, duration, unit):
        self.duration = duration
        self.unit = unit

    def __repr__(self):
        return (
            f"BreakStatement("
            f"duration={self.duration}, "
            f"unit={self.unit})"
        )


class IfStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return (
            f"IfStatement("
            f"condition={self.condition}, "
            f"body={self.body})"
        )


class RepeatStatement(ASTNode):
    def __init__(self, count, body):
        self.count = count
        self.body = body

    def __repr__(self):
        return (
            f"RepeatStatement("
            f"count={self.count}, "
            f"body={self.body})"
        )


# ==========================================
# Expressions
# ==========================================

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return (
            f"BinaryExpression("
            f"left={self.left}, "
            f"operator={self.operator}, "
            f"right={self.right})"
        )


class NumberLiteral(ASTNode):
    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return f"NumberLiteral({self.value})"


class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"StringLiteral({self.value!r})"


class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"