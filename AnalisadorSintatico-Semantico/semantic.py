import pickle
from code_generator import gerar_codigo_mips
from tree import Program, Declaration, Assignment, IfStmt, ForStmt, Block, Expr, BinOp, Term
from var_table import tabela_variaveis, mostrar_tabela, verificar_tabela
from type_check import descobrir_tipo

if __name__ == "__main__":
    with open("ast.pkl", "rb") as f:
        ast = pickle.load(f)

    # 1. Verificações de variáveis
    tabela_declaracao = tabela_variaveis(ast)
    mostrar_tabela()
    verificar_tabela()

    # 2. Verificação de tipos
    def valida_tipos(no):
        if isinstance(no, Program):
            for stmt in no.statements:
                valida_tipos(stmt)
        elif isinstance(no, Declaration) or isinstance(no, Assignment):
            descobrir_tipo(no)
        elif isinstance(no, IfStmt):
            valida_tipos(no.cond)
            valida_tipos(no.block)
        elif isinstance(no, ForStmt):
            valida_tipos(no.init)
            valida_tipos(no.cond)
            valida_tipos(no.update)
            valida_tipos(no.block)
        elif isinstance(no, Block):
            for stmt in no.statements:
                valida_tipos(stmt)
        # Adapte para outros nós se necessário

    print("\n--- Verificação de Tipos ---")
    valida_tipos(ast)
    
    codigo_mips = gerar_codigo_mips(ast, tabela_declaracao)
    with open("output.asm", "w") as f:
        f.write(codigo_mips)
    print("Assembly MIPS gerado em output.asm")