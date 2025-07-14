LEXICO_DIR = AnalisadorLexico
SINTATICO_DIR = AnalisadorSintatico-Semantico

INPUT_FILE ?= file.txt

TOKENS_FILE = tokens.csv
AST_FILE = ast.pkl

all: run

run: run_lexico run_sintatico

run_lexico:
	python3 $(LEXICO_DIR)/main.py $(INPUT_FILE) $(LEXICO_DIR)/$(TOKENS_FILE)

run_sintatico:
	python3 $(SINTATICO_DIR)/parser.py $(LEXICO_DIR)/$(TOKENS_FILE)

clean:
	rm -f $(AST_FILE) $(LEXICO_DIR)/$(TOKENS_FILE)
