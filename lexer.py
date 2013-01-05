import ply.lex as lex

tokens = [
    'TYPE', 'ID', 'SPECIAL',
    'INTEGER',
    'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY',
    'COLON', 'SEMICOLON', 'DOT',
    'ASSIGN',
    'LESS', 'LESSEQUAL', 'EQUAL',
    'INT_COMPLEMENT', 'BOOL_COMPLEMENT',
    'COMMENT', 'KEYWORD',
    'WHITESPACE']

t_ignore = ' \n\f\r\t\v'  # matches t_WHITESPACE

t_TYPE = r'[A-Z][A-Za-z0-9_]*'
t_ID = r'[a-z][A-Za-z0-9_]*'
t_SPECIAL = r'self|SELF_TYPE'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_COLON = r':'
t_SEMICOLON = r';'
t_DOT = r'\.'
t_ASSIGN = r'<-'
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_EQUAL = r'='
t_INT_COMPLEMENT = r'~'
t_BOOL_COMPLEMENT = r'[nN][oO][tT]'
t_KEYWORD = r'class|else|false|fi|if|in|inherits|isvoid|let|loop|pool|then|while|case|esac|new|of|true'
t_WHITESPACE = r'[ \n\f\r\t\v]+'

def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^\0\n]*(\\\n[^\0\n]*)*"'
    t.value = t.value[1:-1]
    return t

def t_COMMENT(t):
    r'--[^\n]+\n|\(\*[^(\*\))]+\*\)'
    pass  # Discard comments


# Create lexer
lex.lex()

# Read source file
with open('example.cl', 'r') as source:
    lex.input(source.read())

# Read tokens
while True:
    token = lex.token()
    if token is None:
        break
    print token
