# **TP_Compilador**

## Especificações

Este projeto consiste no desenvolvimento de um compilador para a disciplina de **Compiladores** da **UFSJ** no período **2025-1**. O compilador será desenvolvido em etapas, com entregas específicas para cada componente do processo de compilação. A primeira entrega será o **Analisador Léxico**.

### Objetivo Geral

Desenvolver um compilador funcional que seja capaz de traduzir uma linguagem de entrada específica baseada em C, mais simplificada, para uma representação intermediária ou código executável, seguindo as etapas clássicas de compilação.

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
## Execução

#### Requisitos
  - Python 3 instalado

  - make instalado

#### Passos

  Entre na pasta TP_Compilador:

  ```bash
  cd TP_Compilador
  ```

  Rode o comando make, passando opcionalmente o arquivo de entrada para o léxico:
  ```bash
  make INPUT_FILE=seu_arquivo.txt
  ```

  Se não passar INPUT_FILE, o padrão será file.txt.

  O analisador léxico irá gerar tokens.csv na pasta AnalisadorLexico.

  O analisador sintático irá ler tokens.csv e gerar ast.pkl.

  Após o processo, você verá no terminal a saída da AST gerada.

  Limpeza dos arquivos gerados

  Para limpar os arquivos executáveis e gerados, rode:

  ```bash
  make clean
  ```

  Isso vai apagar o executável lexer e o arquivo ast.pkl.

  Nota

    O analisador sintático espera o arquivo de tokens CSV dentro da pasta AnalisadorLexico.

    O Makefile está configurado para usar caminhos relativos para facilitar a organização.

## Licença

Este projeto está licenciado sob a [Apache License 2.0](LICENSE). Você pode usá-lo, modificá-lo e distribuí-lo, desde que mantenha os créditos ao autor original.