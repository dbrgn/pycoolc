import ply.lex as lex

tokens = [
    'TYPE', 'ID',

    'INTEGER', 'STRING', 'BOOL',

    'ASSIGN',
    'LESS', 'LESSEQUAL', 'EQUAL',
    'INT_COMPLEMENT', 'NOT',

    'CLASS', 'INHERITS',
    'IF', 'THEN', 'ELSE', 'FI',
    'WHILE', 'LOOP', 'POOL',
    'LET', 'IN',
    'CASE', 'OF', 'ACTION', 'ESAC',
    'NEW',
    'ISVOID']

literals = ['+', '-', '*', '/', ':', ';', '(', ')', '{', '}', '@', '.']

t_ignore = ' \n\f\r\t\v'

t_TYPE = r'[A-Z][A-Za-z0-9_]*'
t_ID = r'[a-z][A-Za-z0-9_]*'

t_ASSIGN = r'<-'
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_EQUAL = r'='
t_INT_COMPLEMENT = r'~'
t_NOT = r'[nN][oO][tT]'

t_CLASS = r'class'
t_INHERITS = r'inherits'
t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_FI = r'fi'
t_WHILE = r'while'
t_LOOP = r'loop'
t_POOL = r'pool'
t_LET = r'let'
t_IN = r'in'
t_CASE = r'case'
t_OF = r'of'
t_ACTION = r'=>'
t_ESAC = r'esac'
t_NEW = r'new'
t_ISVOID = r'isvoid'

def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^\0\n]*(\\\n[^\0\n]*)*"'
    t.value = t.value[1:-1]
    return t

def t_BOOL(t):
    r'true|false'
    return True if t.value == 'true' else False

def t_COMMENT(t):
    r'--[^\n]+\n|\(\*[^(\*\))]+\*\)'
    pass  # Discard comments


# Create lexer
lex.lex()


if __name__ == '__main__':

    # Get file as argument

    import sys
    if len(sys.argv) != 2:
        print('You need to specify a cool source file to read from.', file=sys.stderr)
        sys.exit(1)
    if not sys.argv[1].endswith('.cl'):
        print('Argument needs to be a cool source file ending on ".cl".', file=sys.stderr)
        sys.exit(1)

    sourcefile = sys.argv[1]

    # Read source file

    with open(sourcefile, 'r') as source:
        lex.input(source.read())

    # Read tokens

    while True:
        token = lex.token()
        if token is None:
            break
        print(token)
