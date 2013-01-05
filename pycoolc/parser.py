import ply.yacc as yacc
from . import lexer
tokens = lexer.tokens

# Grammar definitions in BNF form

start = 'program'

def p_program(p):
    """program : classes"""
    pass

def p_classes(p):
    """classes : class
               | classes class"""
    pass

def p_class(p):
    """class : CLASS TYPE inheritance '{' features '}' ';'"""

def p_inheritance(p):
    """inheritance : INHERITS TYPE
                   | empty"""

def p_features(p):
    """features : feature
                | features feature"""

def p_feature(p):
    """feature : ID '(' formals ')' ':' TYPE '{' expr '}' ';'
               | id_def ';'"""

def p_id_defs(p):
    """id_defs : id_def
               | id_def ',' id_defs"""

def p_id_def(p):
    """id_def : ID ':' TYPE assign_opt"""

def p_assign_opt(p):
    """assign_opt : assign
                  | empty"""

def p_assign(p):
    """assign : ASSIGN expr"""

def p_formals(p):
    """formals : formal
               | formal ',' formals"""

def p_formal(p):
    """formal : ID ':' TYPE"""

def p_expr(p):
    """expr : ID assign
            | expr '.' ID '(' params ')'
            | ID '(' params ')'
            | IF expr THEN expr ELSE expr FI
            | WHILE expr LOOP expr POOL
            | '{' block '}'
            | LET ID ':' TYPE assign_opt id_defs IN expr
            | CASE expr OF typeactions ESAC
            | NEW TYPE
            | ISVOID expr
            | expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
            | INT_COMPLEMENT expr
            | expr LESS expr
            | expr LESSEQUAL expr
            | expr EQUAL expr
            | NOT expr
            | '(' expr ')'
            | ID
            | INTEGER
            | STRING
            | BOOL"""
    if len(p) == 2:
        p[0] = p[1]

def p_params(p):
    """params : expr
              | expr ',' params"""

def p_block(p):
    """block : expr ';'
             | expr ';' block"""

def p_typeactions(p):
    """typeactions : typeaction
                   | typeaction typeactions"""
                   
def p_typeaction(p):
    """typeaction : ID ':' TYPE ACTION expr ';'"""

def p_empty(p):
    """empty :"""
    pass

def p_error(p):
    print('Syntax error in input at {!r}'.format(p))


# Create parser
yacc.yacc()


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

    # Read and parse source file

    with open(sourcefile, 'r') as source:
        t = yacc.parse(source.read())

    # Print AST

    print(t)
