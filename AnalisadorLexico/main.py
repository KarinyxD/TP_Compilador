import sys
import csv
import re
from lexer import * # Import all functions and patterns from the lexer.py muodule

# Function to process the input file and extract tokens
def process_file(file, writer):
  anchor = {'line': 1, 'column': 0}
  while (char := file.read(1)): # Read one character at a time
    anchor["column"] += 1
    if char == '\n': # Handle newlines: update line and column
      anchor['line'] += 1
      anchor['column'] = 0
      continue
    if char in [' ', '\t']: # Skip whitespaces
      continue
    if re.match(IDENTIFIER_PATTERN, char):
      identifier(anchor, file, char, writer) # Identifier
    elif re.match(NUMBER_PATTERN, char):
      number(anchor, file, char, writer) # Number
    elif re.match(OPERATOR_PATTERN, char):
      operator(anchor, file, char, writer) # Operator
    elif re.match(LITERAL_PATTERN, char):
      literal(anchor, file, char, writer) #Literal
    elif re.match(SEPARATOR_PATTERN, char):
      separator(anchor, file, char, writer) # Separator
    elif re.match(COMMENT_PATTERN, char):
      comment(anchor, file, char, writer) # Comment
    else: # invalid caracter
        error(anchor, char, file, writer)
  return

# Main function
def main():
  if len(sys.argv) != 3:
    print("Use: python analisadorLexico.py <arquivo_entrada> <arquivo_saida>")
    return
  input_filename = sys.argv[1] 
  csv_filename = sys.argv[2]
  
  try:
    # Open the output csv file for writing, if not exists, to create
    with open(csv_filename, mode='w', newline='') as tokens_file:
      fieldnames = ['id', 'token', 'type', 'line', 'column']
      # Write as a dictionary (columns and keys {'token': 'a', 'type': 'identifier'})
      writer = csv.DictWriter(tokens_file, fieldnames=fieldnames)
      writer.writeheader()

      # Open the input file for reading
      with open(input_filename, 'r') as file:
        process_file(file, writer)
    print(f"Análise léxica concluída. tokens salvos em '{csv_filename}'")
    
  except FileNotFoundError as e:
      print(f"Erro: Arquivo não encontrado - {e.filename}")
  except Exception as e:
      print(f"Erro inesperado: {e}") 
  
  return

# Entry point of the script
if __name__ == "__main__":
  main()