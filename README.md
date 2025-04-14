# **TP_Compilador**

## Especificações

Este projeto consiste no desenvolvimento de um compilador para a disciplina de **Compiladores** da **UFSJ** no período **2025-1**. O compilador será desenvolvido em etapas, com entregas específicas para cada componente do processo de compilação. A primeira entrega será o **Analisador Léxico**.

### Objetivo Geral

Desenvolver um compilador funcional que seja capaz de traduzir uma linguagem de entrada específica baseada em C, mais simplificada, para uma representação intermediária ou código executável, seguindo as etapas clássicas de compilação.

Entrega dia 23/04

### **Especificações do Analisador Léxico**

#### **Entrada**
- Um arquivo de texto contendo o código-fonte da linguagem de entrada.

#### **Saída**
- Um arquivo CSV contendo os tokens identificados, com as seguintes colunas:
  - **id**: Identificador único do token.
  - **token**: O valor do token.
  - **type**: O tipo do token (ex.: identificador, número, operador, etc.).
  - **line**: A linha onde o token foi encontrado.
  - **column**: A coluna onde o token foi encontrado.

| **Categoria**       | **Aceita**                                                               | **Não aceita**                                                                 |
|---------------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| **Identificadores** | Letras, números e `_`, podem começar apenas com letra ou `_`.            | Identificadores começando com números ou contendo caracteres especiais.        |
| **Números**         | Dígitos com ou sem um único ponto decimal.                               | Múltiplos pontos ou caracteres misturados com números.                         |
| **Operadores**      | `+`, `==`, `&&`, `*`, `=`, `^`, `-`, `<=`, `>=`, `!=`, `!`, `<`, `>`, `\|\|`.| Operadores compostos não definidos (`===`, `&\|`, `++`, `--`, etc.).          |
| **Separadores**     | `\n`, `;`, `{`, `}`, `,`, `(`, `)`.                                      | Outros caracteres como `[`, `]`, `:`.                                          |
| **Literais**        | Strings delimitadas por aspas simples ou duplas(pode conter quebra de linha).| Literais não fechados.                                                     |
| **Comentários**     | `#` para uma linha, `#$ ... $#` para múltiplas linhas.                   | Comentários multi-linha não fechados. O caractere `#` imediatamente após alguma palavra. Ex.: `int#comentário`|
| **Erros**           | Caracteres inválidos como `@`, `~`, etc.                                 |                                                                                |

## Licença

Este projeto está licenciado sob a [Apache License 2.0](LICENSE). Você pode usá-lo, modificá-lo e distribuí-lo, desde que mantenha os créditos ao autor original.