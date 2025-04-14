# TP_Compilador

## Especificações

primeira entrega: analisador léxico
- licença (apache,gpl)

Entrega dia 23/04

| **Categoria**       | **Aceita**                                                               | **Não aceita**                                                                 |
|---------------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| **Identificadores** | Letras, números e `_`, podem começar apenas com letra ou `_`.                   | Identificadores começando com números ou contendo caracteres especiais.        |
| **Números**         | Dígitos com ou sem um único ponto decimal.                               | Múltiplos pontos ou caracteres misturados com números.                         |
| **Operadores**      | `+`, `==`, `&&`, `*`, `=`, `^`, `-`, `<=`, `>=`, `!=`, `!`, `<`, `>`, `\|\|`.| Operadores compostos não definidos (`===`, `&|`, `++`, `--`, etc.).          |
| **Separadores**     | `\n`, `;`, `{`, `}`, `,`, `(`, `)`.                                      | Outros caracteres como `[`, `]`, `:`.                                          |
| **Literais**        | Strings delimitadas por aspas simples ou duplas(pode conter quebra de linha).| Literais não fechados.                                                     |
| **Comentários**     | `#` para uma linha, `#$ ... $#` para múltiplas linhas.                   | Comentários multi-linha não fechados. O caractere `#` imediatamente após alguma palavra.|
| **Erros**           | Caracteres inválidos como `@`, `~`, etc.                                 |                                                                                |

## Licença

Este projeto está licenciado sob a [Apache License 2.0](LICENSE). Você pode usá-lo, modificá-lo e distribuí-lo, desde que mantenha os créditos ao autor original.