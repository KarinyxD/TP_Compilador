import re

# deixar mais generico (?)
# recuperacao de erro

# Regular expressions
IDENTIFIER_PATTERN = r'[a-zA-Z_]'
NUMBER_PATTERN = r'[0-9]'
OPERATOR_PATTERN = r'[-+*^/=<>!&|]'
SEPARATOR_PATTERN = r'[\n;{},()]'
LITERAL_PATTERN = r'[\"\']'
ALPHANUM_PATTERN =  r'[a-zA-Z0-9_]'
COMMENT_PATTERN = r'[#]'
COMBINED_PATTERN = rf"{ALPHANUM_PATTERN}|{LITERAL_PATTERN}|[\n]|{SEPARATOR_PATTERN}"

# Token type IDs
TOKEN_TYPE_IDS = {
    'identifier': 1,
    'number': 2,
    'operator': 3,
    'separator': 4,
    'literal': 5,
    'comment': 6,
    'error': 404
}

# Function to process identifier
def identifier(anchor, file, char, writer):
  lookahead = anchor.copy()
  token = char
  while (next_char := file.read(1)):
    if (re.match(ALPHANUM_PATTERN, next_char)): 
      token += next_char
      lookahead['column'] += 1
    elif (re.match(SEPARATOR_PATTERN, next_char)): # At separators, rewind one character
      file.seek(file.tell() - 1) 
      break
    elif (re.match(r'[\t\s]', next_char)): # Stop at whitespace
      lookahead['column'] += 1
      break
    else:
      error(lookahead, next_char)
      break
  print(f"Identificador encontrado: {token}")
  writer.writerow({'id': TOKEN_TYPE_IDS['identifier'], 'token': token, 'type': 'id', 'line': anchor['line'], 'column': anchor['column']})
  anchor['column'] = lookahead['column']
  anchor['line'] = lookahead['line']
  return

# Function to process numbers (integers and decimals)
def number(anchor, file, char, writer):
  lookahead = anchor.copy()
  token = char
  while (next_char := file.read(1)):
    if (re.match(r'[0-9]', next_char)):
      token += next_char
      lookahead['column'] += 1
    elif (re.match(r'[.]', next_char)): # Decimal point
      if '.' in token: # Multiple decimal points are invalid
        error(lookahead, next_char)
        return 
      token += next_char
      lookahead['column'] += 1
    elif (re.match(OPERATOR_PATTERN, next_char) or (re.match(SEPARATOR_PATTERN, next_char))):
      file.seek(file.tell() - 1) # At separators or operators, rewind one character
      break
    elif (re.match(r'[\t\s]', next_char)):
      lookahead['column'] += 1
      break
    else:
      error(lookahead, next_char)
      break
  print(f"Número encontrado: {token}")
  writer.writerow({'id': TOKEN_TYPE_IDS['number'],'token': token, 'type': 'num', 'line': anchor['line'], 'column': anchor['column']})
  anchor['column'] = lookahead['column']
  anchor['line'] = lookahead['line']
  return

# Function to process operators
def operator(anchor, file, char, writer):
  lookahead = anchor.copy()
  token = char
  composed_operators = ['==', '<=', '>=', '!=', '&&', '||']
  while (next_char := file.read(1)):
    if (token + next_char) in composed_operators: # Check for composed operators
      token += next_char
      lookahead['column'] += 1
    elif (re.match(r'[\t\s]', next_char)):
      lookahead['column'] += 1
      break
    elif (re.match(COMBINED_PATTERN, next_char)):
      file.seek(file.tell() - 1) # At alphanumerics, separators and literals, rewind one character
      break
    else:
      error(lookahead, next_char)
      break
  print(f"Operador encontrado: {token}")
  writer.writerow({'id': TOKEN_TYPE_IDS['operator'],'token': token, 'type': 'op', 'line': anchor['line'], 'column': anchor['column']})
  anchor['column'] = lookahead['column']
  anchor['line'] = lookahead['line']
  return

# Function to process separators
def separator(anchor, file, char, writer):
  lookahead = anchor.copy()
  token = char
  while (next_char := file.read(1)):
    if (re.match(COMBINED_PATTERN, next_char)):
      file.seek(file.tell() - 1) # At alphanumerics, separators and literals, rewind one character
      break
    elif (re.match(r'[\t\s]', next_char)):
      lookahead['column'] += 1
      break
    else:
      error(lookahead, next_char)
      break
  print(f"Separador encontrado: {token}")
  writer.writerow({'id': TOKEN_TYPE_IDS['separator'],'token': token, 'type': 'sep', 'line': anchor['line'], 'column': anchor['column']})
  anchor['column'] = lookahead['column']
  anchor['line'] = lookahead['line']
  return

# Function to process literals ('text', "text"), allows line breaks (\n)
def literal(anchor, file, char, writer):
  lookahead = anchor.copy()
  token = char
  start_quote = char # Save start quote
  while (next_char := file.read(1)):
    token += next_char
    lookahead['column'] += 1
    if (next_char == start_quote): # Closing quote when find the second (') or (")
      break
    if next_char == '\n':
      lookahead['line'] += 1
      lookahead['column'] = 0
  if token[-1] != start_quote: # Final check
    error(lookahead, f"Literal não fechado corretamente: {token}")
    return
  print(f"Literal encontrado: {token}")
  writer.writerow({'id': TOKEN_TYPE_IDS['literal'],'token': token, 'type': 'lit', 'line': anchor['line'], 'column': anchor['column']})
  anchor['column'] = lookahead['column']
  anchor['line'] = lookahead['line']
  return

# Function to process comments (single-line # and multi-line #$...$#)
def comment(anchor, file, char, writer):
  lookahead = anchor.copy()
  token = char
  next_char = file.read(1)
  if next_char == '$': # Multi-line comment
    token += next_char
    lookahead['column'] += 1
    while (next_char := file.read(1)):
      token += next_char
      lookahead['column'] += 1
      if next_char == '\n': # Handle newlines: update line and column
        lookahead['line'] += 1
        lookahead['column'] = 0
      if token.endswith('$#'): # End of multi-line comment
        break
  else: # Single-line comment
    while (next_char := file.read(1)):
      token += next_char
      lookahead['column'] += 1
      if next_char == '\n':  # End of sigle-line comment at \n
        lookahead['line'] += 1
        lookahead['column'] = 0
        break
  print(f"Comentário econtrado: {token}")
  writer.writerow({'id': TOKEN_TYPE_IDS['comment'],'token': token, 'type': 'com', 'line': anchor['line'], 'column': anchor['column']})
  anchor['column'] = lookahead['column']
  anchor['line'] = lookahead['line']
  return

# Function to process errors
def error(anchor, char):
  print(f"Erro: caractere inválido '{char}' na linha {anchor['line']}, coluna {anchor['column']}")
  return