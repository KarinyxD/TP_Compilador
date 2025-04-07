import re
import csv

def identifier(anchor, file, char, writer):
  lookahead = anchor.copy()
  token = char
  while (next_char := file.read(1)):
    if (re.match(r'[a-zA-Z0-9_]', next_char)):
      token += next_char
      lookahead['column'] += 1
    elif (re.match(r'[\s]', next_char)):
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
    elif (re.match(r'[-\s;{},()+*/=<>!&|]', next_char)):
      file.seek(file.tell() - 1)
      #separator(lookahead, file, next_char, writer)
      break
    # elif (re.match(r'[-+*/=<>!&|]', next_char)):
    #   operator(lookahead, file, next_char, writer)
    #   break
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
  while (next_char := file.read(1)):
    if (re.match(r'[-+*/=<>!&|]', next_char)):
      token += next_char
      lookahead['column'] += 1
    elif (re.match(r'[\s]', next_char)):
      lookahead['column'] += 1
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
  return

def literal(anchor, file, char, writer):
  lookahead = anchor.copy()
  token = char
  return

def error(anchor, char):
  print(f"Erro: caractere inválido '{char}' na linha {anchor['line']}, coluna {anchor['column']}")
  return


def main():
  csv_filename = 'lista_tokens.csv'

  with open(csv_filename, mode='w', newline='') as tokens_file:
    fieldnames = ['token', 'type', 'line', 'column']
    # Write as a dictionary (columns and keys {'token': 'a', 'type': 'identifier'})
    writer = csv.DictWriter(tokens_file, fieldnames=fieldnames)

    with open('arquivo.txt', 'r') as file:
      anchor = {'line': 1, 'column': 1}
      while (char := file.read(1)):
        if re.match(r'[a-zA-Z_]', char):
          identifier(anchor, file, char, writer)
        elif re.match(r'[0-9]', char):
          number(anchor, file, char, writer)
        elif re.match(r'[-+*/=<>!&|]', char):
          operator(anchor, file, char, writer)
        elif re.match(r'[\s\n\t;{},()]', char):
          separator(anchor, file, char, writer)
        elif re.match(r'[\"\']', char):
          literal(anchor, file, char, writer)
        # elif char == 'b':
        #   comentario()
        # anchor['line'] += 1
        # anchor['column'] += 1
    return

main()
    