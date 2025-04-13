# Nome do executável
EXEC = lexer

# Arquivo principal
MAIN = main.py

# Argumentos padrão para o programa
INPUT_FILE = file.txt
OUTPUT_FILE = tokens.csv

# Regra padrão: cria um "executável" simbólico
all: $(EXEC)

# Cria um alias para o programa principal
$(EXEC): $(MAIN)
	echo "#!/bin/bash\npython3 $(MAIN) \$$@" > $(EXEC)
	chmod +x $(EXEC)

# Executa o programa com os argumentos padrão
run: $(EXEC)
	./$(EXEC) $(INPUT_FILE) $(OUTPUT_FILE)

# Limpa o executável gerado
clean:
	rm -f $(EXEC)