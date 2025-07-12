import pickle
from tree import Program, Declaration, Assignment, IfStmt, ForStmt, Block, Expr, BinOp, Term

# Tabela de declaração
tabela_declaracao = {}
RESERVADAS = {"True", "False", "int", "float", "char", "bool", "if", "for", "else", "return"}

def declarar_variavel(nome, linha, tipo):
    if nome not in tabela_declaracao:
        tabela_declaracao[nome] = {
            "linhas_declaracao": [linha],
            "linhas_uso": [],
            "tipo": tipo,
            "linha_inicializacao": None
        }
    else:
        tabela_declaracao[nome]["linhas_declaracao"].append(linha)

def usar_variavel(nome, linha):
    if nome not in tabela_declaracao:
        tabela_declaracao[nome] = {
            "linhas_declaracao": [],
            "linhas_uso": [linha],
            "tipo": None,
            "linha_inicializacao": None
        }
    else:
        tabela_declaracao[nome]["linhas_uso"].append(linha)
        
def inicializar_variavel(nome, linha):
    if nome in tabela_declaracao and tabela_declaracao[nome]["linha_inicializacao"] is None:
        tabela_declaracao[nome]["linha_inicializacao"] = linha

def mostrar_tabela():
    print("Variável | Linha Declaração | Linhas Uso | Tipo | Linha Inicialização")
    for nome, info in tabela_declaracao.items():
        print(f"{nome} | {info['linhas_declaracao']} | {info['linhas_uso']} | {info['tipo']} | {info['linha_inicializacao']}")
        
        
def tabela_variaveis(no):
    if isinstance(no, Program):
        for stmt in no.statements:
            tabela_variaveis(stmt)
            
    elif isinstance(no, Declaration):
        declarar_variavel(no.nome, no.linha, no.tipo)
        if no.expr:
            inicializar_variavel(no.nome, no.linha)
            tabela_variaveis(no.expr)

    elif isinstance(no, Assignment):
        if no.identificador not in tabela_declaracao:
            tabela_declaracao[no.identificador] = {
                "linhas_declaracao": [],
                "linhas_uso": [],
                "tipo": None,
                "linha_inicializacao": no.linha
            }
        else:
            inicializar_variavel(no.identificador, no.linha)
        tabela_variaveis(no.expr)

    elif isinstance(no, IfStmt):
        tabela_variaveis(no.cond)
        tabela_variaveis(no.block)

    elif isinstance(no, ForStmt):
       tabela_variaveis(no.init)
       tabela_variaveis(no.cond)
       tabela_variaveis(no.update)
       tabela_variaveis(no.block)

    elif isinstance(no, Block):
        for stmt in no.statements:
           tabela_variaveis(stmt)

    elif isinstance(no, Expr):
        tabela_variaveis(no.value)

    elif isinstance(no, BinOp):
        tabela_variaveis(no.left)
        tabela_variaveis(no.right)

    elif isinstance(no, Term):
        if isinstance(no.value, str) and no.value.isidentifier() and no.value not in RESERVADAS:
            usar_variavel(no.value, no.linha)
            
def verificar_tabela():
    print("\n--- Verificação da Tabela de Variáveis ---")
    for nome, info in tabela_declaracao.items():
        # 1. Inicializada ou usada mas não declarada
        if not info["linhas_declaracao"] and (info["linha_inicializacao"] is not None or info["linhas_uso"]):
            print(f"ERRO: Variável '{nome}' foi inicializada mas sem declaração.")

        # 2. Declarada mais de uma vez
        if len(info["linhas_declaracao"]) > 1:
            print(f"ERRO: Variável '{nome}' declarada mais de uma vez nas linhas {info['linhas_declaracao']}")

        # 3. Declarada mas não utilizada
        if info["linhas_declaracao"] and not info["linhas_uso"]:
            print(f"AVISO: Variável '{nome}' declarada na linha {info['linhas_declaracao']} mas nunca utilizada.")


    
# Exemplo de uso:
# analisar_ast(ast)
# mostrar_tabela()