from tree import Program, Declaration, Assignment, IfStmt, ForStmt, Block, Expr, BinOp, Term
from type_check import descobrir_tipo
from var_table import tabela_declaracao

# Tabela de declaração      
label_counter = [0]  # Para gerar rótulos únicos


label_counter = [0]

def novo_label(base):
    label_counter[0] += 1
    return f"{base}_{label_counter[0]}"

def gerar_codigo_mips(ast, tabela_declaracao):
    codigo = ".data\n"
    for var, info in tabela_declaracao.items():
        tipo = info["tipo"]
        if tipo == "char":
            codigo += f"{var}: .byte 0\n"
        elif tipo == "float":
            codigo += f"{var}: .float 0.0\n"
        elif tipo == "bool":
            codigo += f"{var}: .byte 0\n"
        else:
            codigo += f"{var}: .word 0\n"
    codigo += "\n.text\n.globl main\nmain:\n"
    codigo += gerar_codigo_mips_rec(ast)
    return codigo

def gerar_codigo_mips_rec(no, reg_stack=None):
    if reg_stack is None:
        reg_stack = ["$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7", "$t8", "$t9"]

    codigo = ""

    if isinstance(no, Program):
        for stmt in no.statements:
            codigo += gerar_codigo_mips_rec(stmt, reg_stack)
        codigo += "li $v0, 10\nsyscall\n"
        return codigo

    elif isinstance(no, Declaration):
        if no.expr:
            expr_codigo = gerar_codigo_mips_rec(no.expr, reg_stack)
            tipo = no.tipo
            if tipo == "char" or tipo == "bool":
                codigo += expr_codigo
                codigo += f"sb {reg_stack[0]}, {no.nome}\n"
            elif tipo == "float":
                codigo += expr_codigo
                codigo += f"swc1 $f0, {no.nome}\n"
            else:  # int
                codigo += expr_codigo
                codigo += f"sw {reg_stack[0]}, {no.nome}\n"
        return codigo

    elif isinstance(no, Assignment):
        expr_codigo = gerar_codigo_mips_rec(no.expr, reg_stack)
        codigo += expr_codigo
        codigo += f"sw {reg_stack[0]}, {no.identificador}\n"
        return codigo

    elif isinstance(no, Expr):
        return gerar_codigo_mips_rec(no.value, reg_stack)

    elif isinstance(no, BinOp):
        tipo_esq = descobrir_tipo(no.left)
        tipo_dir = descobrir_tipo(no.right)
        op = no.op

        # Operações com float
        if tipo_esq == "float" or tipo_dir == "float":
            left_code = gerar_codigo_mips_rec(no.left, reg_stack[1:])
            right_code = gerar_codigo_mips_rec(no.right, reg_stack[2:])
            codigo = ""

            if tipo_esq == "int":
                codigo += left_code
                codigo += f"mtc1 {reg_stack[0]}, $f1\ncvt.s.w $f1, $f1\n"
            else:
                codigo += left_code
                codigo += f"mov.s $f1, $f0\n"

            if tipo_dir == "int":
                codigo += right_code
                codigo += f"mtc1 {reg_stack[0]}, $f2\ncvt.s.w $f2, $f2\n"
            else:
                codigo += right_code
                codigo += f"mov.s $f2, $f0\n"

            if op == "+":
                codigo += "add.s $f0, $f1, $f2\n"
            elif op == "*":
                codigo += "mul.s $f0, $f1, $f2\n"
            return codigo

        # Operações com int, bool, char (usando registradores inteiros)
        else:
            left_reg = reg_stack[1]
            right_reg = reg_stack[2]
            result_reg = reg_stack[0]

            left_code = gerar_codigo_mips_rec(no.left, reg_stack[1:])
            right_code = gerar_codigo_mips_rec(no.right, reg_stack[2:])

            codigo = (
                left_code + f"move {left_reg}, {reg_stack[0]}\n" +
                right_code + f"move {right_reg}, {reg_stack[0]}\n"
            )

            if op == "+":
                codigo += f"add {result_reg}, {left_reg}, {right_reg}\n"
            elif op == "*":
                codigo += f"mul {result_reg}, {left_reg}, {right_reg}\n"
            elif op == "&&":
                codigo += f"and {result_reg}, {left_reg}, {right_reg}\n"
            elif op == "<":
                codigo += f"slt {result_reg}, {left_reg}, {right_reg}\n"
            return codigo

    elif isinstance(no, Term):
        if no.value == "True":
            return "li $t0, 1\n"
        elif no.value == "False":
            return "li $t0, 0\n"
        elif isinstance(no.value, str) and no.value.isdigit():
            return f"li $t0, {no.value}\n"
        elif isinstance(no.value, str) and no.value.startswith("'") and no.value.endswith("'"):
            return f"li $t0, {ord(no.value[1])}\n"
        elif isinstance(no.value, str):
            try:
                float(no.value)
                return f"li.s $f0, {no.value}\n"
            except ValueError:
                tipo = tabela_declaracao.get(no.value, {}).get("tipo", "int")
                if tipo == "char" or tipo == "bool":
                    return f"lb $t0, {no.value}\n"
                elif tipo == "float":
                    return f"lwc1 $f0, {no.value}\n"
                else:
                    return f"lw $t0, {no.value}\n"
        elif isinstance(no.value, int):
            return f"li $t0, {no.value}\n"
        elif isinstance(no.value, float):
            return f"li.s $f0, {no.value}\n"
        else:
            return ""

    elif isinstance(no, IfStmt):
        cond_codigo = gerar_codigo_mips_rec(no.cond, reg_stack)
        bloco_codigo = gerar_codigo_mips_rec(no.block, reg_stack)
        end_label = novo_label("endif")
        codigo += cond_codigo
        codigo += f"beq $t0, $zero, {end_label}\n"
        codigo += bloco_codigo
        codigo += f"{end_label}:\n"
        return codigo

    elif isinstance(no, ForStmt):
        start_label = novo_label("for_start")
        end_label = novo_label("for_end")

        init = gerar_codigo_mips_rec(no.init, reg_stack)
        cond = gerar_codigo_mips_rec(no.cond, reg_stack)
        update = gerar_codigo_mips_rec(no.update, reg_stack)
        bloco = gerar_codigo_mips_rec(no.block, reg_stack)

        codigo += init
        codigo += f"{start_label}:\n"
        codigo += cond
        codigo += f"beq $t0, $zero, {end_label}\n"
        codigo += bloco
        codigo += update
        codigo += f"j {start_label}\n"
        codigo += f"{end_label}:\n"
        return codigo

    elif isinstance(no, Block):
        for stmt in no.statements:
            codigo += gerar_codigo_mips_rec(stmt, reg_stack)
        return codigo

    return ""
