# Analisador Léxico

Este é um analisador léxico desenvolvido em Python. Ele processa um arquivo de entrada contendo código-fonte e gera um arquivo CSV com os tokens identificados.

## Pré-requisitos

Certifique-se de que você tem o seguinte instalado no seu sistema:

- Python 3
- Make (ferramenta de automação)

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

├── main.py # Arquivo principal que executa o analisador léxico 

├── lexer.py # Contém as funções e padrões de análise léxica 

├── Makefile # Arquivo Makefile para automação 

├── file.txt # Arquivo de entrada de exemplo 

├── tokens.csv # Arquivo de saída gerado (tokens)


## Instruçoes de Execuçao
## Como usar o Makefile

O `Makefile` foi configurado para facilitar a execução do programa. Ele contém os seguintes passos:

#### 1. **Gerar o executável**

Para criar o executável simbólico (`lexer`), execute:
```bash
make
```

#### 2. **Executar o programa**

Para executar o programa com os argumentos padrão (file.txt como entrada e tokens.csv como saída), use:
```bash
make run
```

Se você quiser executar o programa com um arquivo de entrada ou saída diferente, pode usar o executável diretamente após criá-lo com make:
```bash
./lexer <arquivo_entrada> <arquivo_saida>
```

#### 3. **Limpar o executável**
Para remover o executável gerado (lexer), use:
```bash
make clean
```

#### Observações:
Certifique-se de que o arquivo de entrada exista antes de executar o programa. O arquivo de saída será criado automaticamente, caso não exista, mas é recomendado que ele já esteja presente para evitar possíveis problemas.


