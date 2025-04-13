import sys
import csv
import re
from lexer import *

def process_file(file, writer):
  anchor = {'line': 1, 'column': 0}
  while (char := file.read(1)):
    anchor["column"] += 1
    if char == '\n':
      anchor['line'] += 1
      anchor['column'] = 0
      continue
    if char in [' ', '\t']: 
      continue
    if re.match(IDENTIFIER_PATTERN, char):
      identifier(anchor, file, char, writer)
    elif re.match(NUMBER_PATTERN, char):
      number(anchor, file, char, writer)
    elif re.match(OPERATOR_PATTERN, char):
      operator(anchor, file, char, writer)
    elif re.match(LITERAL_PATTERN, char):
      literal(anchor, file, char, writer)
    elif re.match(SEPARATOR_PATTERN, char):
      separator(anchor, file, char, writer)
    elif re.match(COMMENT_PATTERN, char):
      comment(anchor, file, char, writer)
    else: # invalid caracter
        error(anchor, char)
  return

def main():
  if len(sys.argv) != 3:
    print("Use: python analisadorLexico.py <arquivo_entrada> <arquivo_saida>")
    return
  input_filename = sys.argv[1]
  csv_filename = sys.argv[2]
  
  try:
    with open(csv_filename, mode='w', newline='') as tokens_file:
      fieldnames = ['id', 'token', 'type', 'line', 'column']
      # Write as a dictionary (columns and keys {'token': 'a', 'type': 'identifier'})
      writer = csv.DictWriter(tokens_file, fieldnames=fieldnames)
      writer.writeheader()

      with open(input_filename, 'r') as file:
        process_file(file, writer)
    print(f"Análise léxica concluída. tokens salvos em '{csv_filename}'")
    
  except FileNotFoundError as e:
      print(f"Erro: Arquivo não encontrado - {e.filename}")
  except Exception as e:
      print(f"Erro inesperado: {e}") 
  
  return


if __name__ == "__main__":
  main()