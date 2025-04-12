import re
import csv
# aceitar outros numeros, como elevados e numero negativos
# adicionar o ID no csv (?)
# deixar mais generico (?)
IDENTIFIER_PATTERN = r'[a-zA-Z_]'
NUMBER_PATTERN = r'[0-9]'
OPERATOR_PATTERN = r'[-+*/=<>!&|]'
SEPARATOR_PATTERN = r'[\n;{},()]'
LITERAL_PATTERN = r'[\"\']'
ALPHANUM_PATTERN =  r'[a-zA-Z0-9_]'

def identifier(anchor, file, char, writer):
  lookahead = anchor.copy()
  token = char
  while (next_char := file.read(1)):
    if (re.match(ALPHANUM_PATTERN, next_char)):
      token += next_char
      lookahead['column'] += 1
    elif (re.match(SEPARATOR_PATTERN, next_char)):
      file.seek(file.tell() - 1)
      break
    elif (re.match(r'[\t\s]', next_char)):
      lookahead['column'] += 1
      break
    else:
      error(lookahead, next_char)
      break
  print(f"Identificador encontrado: {token}")
  writer.writerow({'token': token, 'type': 'identifier', 'line': anchor['line'], 'column': anchor['column']})
  anchor['column'] = lookahead['column']
  anchor['line'] = lookahead['line']
  return

def number(anchor, file, char, writer):
  lookahead = anchor.copy()
  token = char
  while (next_char := file.read(1)):
    if (re.match(r'[0-9]', next_char)):
      token += next_char
      lookahead['column'] += 1
    elif (re.match(r'[.]', next_char)):
      if '.' in token:
        error(lookahead, next_char)
        return 
      token += next_char
      lookahead['column'] += 1
    elif (re.match(OPERATOR_PATTERN, next_char) or (re.match(SEPARATOR_PATTERN, next_char))):
      file.seek(file.tell() - 1)
      break
    elif (re.match(r'[\t\s]', next_char)):
      lookahead['column'] += 1
      break
    else:
      error(lookahead, next_char)
      break
  print(f"Número encontrado: {token}")
  writer.writerow({'token': token, 'type': 'number', 'line': anchor['line'], 'column': anchor['column']})
  anchor['column'] = lookahead['column']
  anchor['line'] = lookahead['line']
  return

def operator(anchor, file, char, writer):
  lookahead = anchor.copy()
  token = char
  composed_operators = ['==', '<=', '>=', '!=', '&&', '||']
  while (next_char := file.read(1)):
    if (token + next_char) in composed_operators:
      token += next_char
      lookahead['column'] += 1
    elif (re.match(r'[\t\s]', next_char)):
      lookahead['column'] += 1
      break
    elif (re.match(ALPHANUM_PATTERN, next_char) or re.match(SEPARATOR_PATTERN, next_char) or re.match(LITERAL_PATTERN, next_char)):
      file.seek(file.tell() - 1)
      break
    else:
      error(lookahead, next_char)
      break
  print(f"Operador encontrado: {token}")
  writer.writerow({'token': token, 'type': 'operator', 'line': anchor['line'], 'column': anchor['column']})
  anchor['column'] = lookahead['column']
  anchor['line'] = lookahead['line']
  return

def separator(anchor, file, char, writer):
  lookahead = anchor.copy()
  token = char
  COMBINED_PATTERN = rf"{ALPHANUM_PATTERN}|{LITERAL_PATTERN}|[\n]|{SEPARATOR_PATTERN}"
  while (next_char := file.read(1)):
    if (re.match(COMBINED_PATTERN, next_char)):
      file.seek(file.tell() - 1)
      break
    elif (re.match(r'[\t\s]', next_char)):
      lookahead['column'] += 1
      break
    else:
      error(lookahead, next_char)
      break
  print(f"Separador encontrado: {token}")
  writer.writerow({'token': token, 'type': 'separator', 'line': anchor['line'], 'column': anchor['column']})
  anchor['column'] = lookahead['column']
  anchor['line'] = lookahead['line']
  return

def literal(anchor, file, char, writer):
  lookahead = anchor.copy()
  token = char
  start_quote = char
  while (next_char := file.read(1)):
    token += next_char
    lookahead['column'] += 1
    if (next_char == start_quote):
      break
    if next_char == '\n':
      lookahead['line'] += 1
      lookahead['column'] = 0
  if token[-1] != start_quote:  # O último caractere deve ser o mesmo que o de abertura
    error(lookahead, f"Literal não fechado corretamente: {token}")
    return
      
  print(f"Literal encontrado: {token}")
  writer.writerow({'token': token, 'type': 'literal', 'line': anchor['line'], 'column': anchor['column']})
  anchor['column'] = lookahead['column']
  anchor['line'] = lookahead['line']
  return

def error(anchor, char):
  print(f"Erro: caractere inválido '{char}' na linha {anchor['line']}, coluna {anchor['column']}")
  return

def update_position(anchor, char):
  if char == '\n':
      anchor['line'] += 1
      anchor['column'] = 0
  else:
      anchor['column'] += 1
      

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
    else: # invalid caracter
        error(anchor, char)
    # elif char == 'b':
    #   comentario()
  return

def main():
  csv_filename = 'lista_tokens.csv'
  input_filename = 'arquivo.txt'
  try:
    with open(csv_filename, mode='w', newline='') as tokens_file:
      fieldnames = ['token', 'type', 'line', 'column']
      # Write as a dictionary (columns and keys {'token': 'a', 'type': 'identifier'})
      writer = csv.DictWriter(tokens_file, fieldnames=fieldnames)
      
      with open(input_filename, 'r') as file:
        process_file(file, writer)
    
  except FileNotFoundError as e:
      print(f"Erro: Arquivo não encontrado - {e.filename}")
  except Exception as e:
      print(f"Erro inesperado: {e}") 
  
  return


main()
    