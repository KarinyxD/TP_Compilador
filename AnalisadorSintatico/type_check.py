import pickle
from tree import Program, Declaration, Assignment, IfStmt, ForStmt, Block, Expr, BinOp, Term
from semantic2 import tabela_declaracao, declarar_variavel, usar_variavel, inicializar_variavel, mostrar_tabela, tabela_variaveis

# Operador +
tabela_mais = {
    ("int", "int"): "int",
    ("int", "float"): "float",
    ("float", "int"): "float",
    ("float", "float"): "float",
    ("char", "char"): "char",
}

# Operador *
tabela_vezes = {
    ("int", "int"): "int",
    ("int", "float"): "float",
    ("float", "int"): "float",
    ("float", "float"): "float",
}

# Operador &&
tabela_and = {
    ("bool", "bool"): "bool",
}

def valida_operacao(op, tipo1, tipo2):
    if op == "+":
        return tabela_mais.get((tipo1, tipo2), "erro")
    elif op == "*":
        return tabela_vezes.get((tipo1, tipo2), "erro")
    elif op == "&&":
        return tabela_and.get((tipo1, tipo2), "erro")
    else:
        return "erro"
from type_check import valida_operacao

def descobrir_tipo(no):
    if isinstance(no, Term):
        # Se for literal, retorne o tipo correspondente
        if isinstance(no.value, str):
            if no.value.isdigit():
                return "int"
            # Adapte para float, char, bool, etc.
            if no.value in ("True", "False"):
                return "bool"
            if no.value.startswith("'") and no.value.endswith("'"):
                return "char"
            # Se for variável, busque na tabela_declaracao
            if no.value in tabela_declaracao:
                return tabela_declaracao[no.value]["tipo"]
        # Adapte para outros casos
        return None

    elif isinstance(no, BinOp):
        tipo_esq = descobrir_tipo(no.left)
        tipo_dir = descobrir_tipo(no.right)
        tipo_resultado = valida_operacao(no.op, tipo_esq, tipo_dir)
        if tipo_resultado == "erro":
            print(f"ERRO: Operação '{no.op}' inválida entre '{tipo_esq}' e '{tipo_dir}'")
        return tipo_resultado

    elif isinstance(no, Expr):
        return descobrir_tipo(no.value)
    
    elif isinstance(no, Declaration):
      declarar_variavel(no.nome, no.linha, no.tipo)
      if no.expr:
          tipo_expr = descobrir_tipo(no.expr)
          if tipo_expr != no.tipo:
              print(f"ERRO: Tipo incompatível na declaração de '{no.nome}' na linha {no.linha}: esperado '{no.tipo}'")
          inicializar_variavel(no.nome, no.linha)
          usar_variavel(no.nome, no.linha)
          tabela_variaveis(no.expr)

    elif isinstance(no, Assignment):
        tipo_var = tabela_declaracao.get(no.identificador, {}).get("tipo")
        tipo_expr = descobrir_tipo(no.expr)
        if tipo_var and tipo_expr and tipo_var != tipo_expr:
            print(f"ERRO: Tipo incompatível na atribuição para '{no.identificador}' na linha {no.linha}: esperado '{tipo_var}")
    return None
  
  
# Exemplos de uso:
#print(valida_operacao("+", "int", "float"))   # float
#print(valida_operacao("*", "int", "char"))   # erro
#print(valida_operacao("&&", "bool", "bool")) # bool