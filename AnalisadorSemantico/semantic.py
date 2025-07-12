from AnalisadorSintatico.tree import *

TYPE_TABLE = {
    ('int', 'int', '+'): 'int',
    ('int', 'int', '-'): 'int',
    ('int', 'int', '*'): 'int',
    ('int', 'int', '/'): 'int',
    ('float', 'float', '+'): 'float',
    ('float', 'float', '-'): 'float',
    ('float', 'float', '*'): 'float',
    ('float', 'float', '/'): 'float',
    ('int', 'float', '+'): 'float',
    ('float', 'int', '+'): 'float',
    # Adicione mais combinações conforme necessário
}

class SemanticError(Exception):
    pass

class SymbolTable:
    def __init__(self):
        self.table = {}

    def declare(self, name, tipo):
        if name in self.table:
            raise SemanticError(f"Variável '{name}' já declarada.")
        self.table[name] = tipo

    def get(self, name):
        if name not in self.table:
            raise SemanticError(f"Variável '{name}' não declarada.")
        return self.table[name]

class SemanticAnalyzer:
    def __init__(self):
        self.symbols = SymbolTable()

    def analyze(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.analyze(stmt)
        elif isinstance(node, Declaration):
            self.symbols.declare(node.identificador, node.tipo)
            if node.expr:
                self.analyze(node.expr)
        elif isinstance(node, Assignment):
            tipo = self.symbols.get(node.identificador)
            self.analyze(node.expr)
        elif isinstance(node, IfStmt):
            self.analyze(node.cond)
            self.analyze(node.bloco)
        elif isinstance(node, ForStmt):
            self.analyze(node.init)
            self.analyze(node.cond)
            self.analyze(node.update)
            self.analyze(node.bloco)
        elif isinstance(node, Block):
            for stmt in node.statements:
                self.analyze(stmt)
        elif isinstance(node, Expr):
            self.analyze(node.value)
        elif isinstance(node, BinOp):
            self.analyze(node.left)
            self.analyze(node.right)
        elif isinstance(node, Term):
            pass  # Aqui você pode checar se o termo é uma variável e se foi declarada
        else:
            pass  # Outros casos

# Exemplo de uso:
# from parser import Parser, load_tokens_from_csv
# tokens = load_tokens_from_csv("tokens.csv")
# parser = Parser(tokens)
# ast = parser.parse()
# analyzer = SemanticAnalyzer()
# analyzer.analyze(ast)