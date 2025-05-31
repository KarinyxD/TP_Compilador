import csv
import sys
import pickle
from tree import *

# Estrutura para representar um token
class Token:
    def __init__(self, id, token, type, line, column):
        self.id = int(id)
        self.token = token
        self.type = type
        self.line = int(line)
        self.column = int(column)

    def __repr__(self):
        return f"Token({self.token}, {self.type}, line={self.line}, col={self.column})"

# Classe principal do Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None

    def match(self, expected_token):
        token = self.peek()
        if token and token.token == expected_token:
            self.current += 1
            return token
        self.error(f"Esperado '{expected_token}', encontrado '{token.token if token else 'EOF'}'")
        return None

    def match_type(self, expected_type):
        token = self.peek()
        if token and token.type == expected_type:
            self.current += 1
            return token
        self.error(f"Esperado tipo '{expected_type}', encontrado '{token.type if token else 'EOF'}'")
        return None

    def error(self, message):
        token = self.peek()
        if token:
            print(f"[Erro] Linha {token.line}, Coluna {token.column}: {message}")
        else:
            print(f"[Erro] Fim inesperado do arquivo: {message}")
        sys.exit(1)

    def parse(self):
        statements = []
        while self.peek():
            stmt = self.parse_stmt()
            if stmt:
                statements.append(stmt)
        return Program(statements)

    def parse_stmt(self):
      # Pula todos os comentários antes de analisar o próximo comando
      while self.peek() and self.peek().type == "com":
        self.current += 1

      token = self.peek()
      if not token:
        return

      if token.type == "id":
        if token.token == "int":
          node = self.parse_declaration()
          self.match(";")  # consumir ';' após declaração
          return node
        elif token.token == "if":
          return self.parse_if()
        elif token.token == "for":
          return self.parse_for()
        elif token.token == "print":
          node = self.parse_print()
          self.match(";")  # consumir ';' após declaração
          return node
        else:
          node = self.parse_assignment()
          self.match(";")  # consumir ';' após declaração
          return node
      else:
        # Se chegar aqui, comando inválido para simplificação
        print(f"[Erro] Linha {token.line}, Coluna {token.column}: Comando inválido: '{token.token}'")
        self.current += 1  # Avança para tentar continuar a análise
        return

    def parse_declaration(self):
        tipo = self.match_type("id").token
        identificador = self.match_type("id").token
        self.match("=")
        expr = self.parse_expr()
        return Declaration(tipo, identificador, expr)

    def parse_assignment(self):
        identificador = self.match_type("id").token
        self.match("=")
        expr = self.parse_expr()
        return Assignment(identificador, expr)

    def parse_if(self):
        self.match("if")
        self.match("(")
        cond = self.parse_expr()
        self.match(")")
        bloco = self.parse_block()
        return IfStmt(cond, bloco)

    def parse_for(self):
        self.match("for")
        self.match("(")
        init = self.parse_declaration()
        self.match(";")
        cond = self.parse_expr()
        self.match(";")
        update = self.parse_assignment()
        self.match(")")
        bloco = self.parse_block()
        return ForStmt(init, cond, update, bloco)

    def parse_print(self):
        self.match("print")
        self.match("(")
        lit = self.match_type("lit").token
        self.match(")")
        return PrintStmt(lit)

    def parse_block(self):
        self.match("{")
        stmts = []
        while self.peek() and self.peek().token != "}":
            stmt = self.parse_stmt()
            if stmt:
                stmts.append(stmt)
        self.match("}")
        return Block(stmts)

    def parse_expr(self):
        left = self.parse_term()
        while self.peek() and self.peek().token in ("+", "-", "*", "/", ">", "<", "==", "!="):
            op = self.match(self.peek().token).token
            right = self.parse_term()
            left = BinOp(op, left, right)
        return Expr(left)

    def parse_term(self):
        token = self.peek()
        if token.type in ("id", "num", "lit"):
            self.current += 1
            return Term(token.token)
        elif token.token == "(":
            self.match("(")
            expr = self.parse_expr()
            self.match(")")
            return expr
        else:
            self.error("Expressão inválida")

# Função principal
def load_tokens_from_csv(file_path):
    tokens = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tokens.append(Token(**row))
    return tokens

def main():
    if len(sys.argv) != 2:
        print("Uso: python parser.py <tokens.csv>")
        return

    tokens = load_tokens_from_csv(sys.argv[1])
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST gerada:")
    ast.pretty_print()
    # Salvar em arquivo
    with open("ast.pkl", "wb") as f:
        pickle.dump(ast, f)
    print("AST salva em ast.pkl")
    print("Análise sintática concluída com sucesso.")

if __name__ == "__main__":
    main()
