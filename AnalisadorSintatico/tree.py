# tree.py

class Program:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"

    def pretty_print(self, indent=""):
        print("Program")
        for stmt in self.statements:
            stmt.pretty_print(indent + "├── ")


class Declaration:
    def __init__(self, tipo, identificador, expr):
        self.tipo = tipo
        self.identificador = identificador
        self.expr = expr

    def __repr__(self):
        return f"Declaration({self.tipo}, {self.identificador}, {self.expr})"

    def pretty_print(self, indent=""):
        print(f"{indent}Declaration ({self.tipo} {self.identificador})")
        self.expr.pretty_print(indent + "│   ")


class Assignment:
    def __init__(self, identificador, expr):
        self.identificador = identificador
        self.expr = expr

    def __repr__(self):
        return f"Assignment({self.identificador}, {self.expr})"

    def pretty_print(self, indent=""):
        print(f"{indent}Assignment ({self.identificador})")
        self.expr.pretty_print(indent + "│   ")


class IfStmt:
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

    def __repr__(self):
        return f"If({self.cond}, {self.block})"

    def pretty_print(self, indent=""):
        print(f"{indent}If")
        print(f"{indent}│   Condition:")
        self.cond.pretty_print(indent + "│   │   ")
        print(f"{indent}│   Block:")
        self.block.pretty_print(indent + "│   │   ")


class ForStmt:
    def __init__(self, init, cond, update, block):
        self.init = init
        self.cond = cond
        self.update = update
        self.block = block

    def __repr__(self):
        return f"For({self.init}, {self.cond}, {self.update}, {self.block})"

    def pretty_print(self, indent=""):
        print(f"{indent}For")
        self.init.pretty_print("│   │   ")
        print(f"{indent}│   Condition:")
        self.cond.pretty_print(indent + "│   │   ")
        self.update.pretty_print("│   │   ")
        print(f"{indent}│   Block:")
        self.block.pretty_print(indent + "│   │   ")


class PrintStmt:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Print({self.value})"

    def pretty_print(self, indent=""):
        print(f"{indent}Print")
        self.value.pretty_print(indent + "│   ")


class Block:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"

    def pretty_print(self, indent=""):
        for stmt in self.statements:
            stmt.pretty_print(indent)


class Expr:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Expr({self.value})"

    def pretty_print(self, indent=""):
        print(f"{indent}Expr")
        self.value.pretty_print(indent + "│   ")


class BinOp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinOp({self.op}, {self.left}, {self.right})"

    def pretty_print(self, indent=""):
        print(f"{indent}BinOp ({self.op})")
        self.left.pretty_print(indent + "│   ")
        self.right.pretty_print(indent + "│   ")


class Term:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Term({self.value})"

    def pretty_print(self, indent=""):
        print(f"{indent}Term ({self.value})")


