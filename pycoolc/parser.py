from collections import namedtuple
import ply.yacc as yacc
from . import lexer
tokens = lexer.tokens

# AST namedtuples

Class = namedtuple('Class', 'name inherits features')
Feature = namedtuple('Feature', 'name type formals expr')
Block = namedtuple('Block', 'elements')

# Grammar definitions in BNF form

def p_program(p):
    """program : classes"""
    p[0] = p[1]

def p_classes(p):
    """classes : class
               | class classes"""
    p[0] = (p[1],)
    if len(p) == 3:
        p[0] += p[2]

def p_class(p):
    """class : CLASS TYPE inheritance '{' features '}' ';'"""
    p[0] = Class(name=p[2], inherits=p[3], features=p[5])

def p_inheritance(p):
    """inheritance : INHERITS TYPE
                   | empty"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[2]
    else:
        raise SyntaxError('Invalid number of symbols')

def p_features(p):
    """features : feature
                | feature features"""

    p[0] = (p[1],)
    if len(p) == 3:
        p[0] += p[2]
    
def p_feature(p):
    """feature : ID '(' ')' ':' TYPE '{' expr '}' ';'"""
    #"""feature : ID '(' formals ')' ':' TYPE '{' expr '}' ';'
    #           | id_def ';'"""
    p[0] = Feature(name=p[1], type=p[5], formals=None, expr=p[7])

#def p_id_defs(p):
#    """id_defs : id_def
#               | id_def ',' id_defs"""

#def p_id_def(p):
#    """id_def : ID ':' TYPE assign_opt"""

#def p_assign_opt(p):
#    """assign_opt : assign
#                  | empty"""

#def p_assign(p):
#    """assign : ASSIGN expr"""

#def p_formals(p):
#    """formals : formal
#               | formal ',' formals"""

#def p_formal(p):
#    """formal : ID ':' TYPE"""

def p_expr(p):
    """expr : INTEGER
            | '{' block '}'
    """
    first_token = p.slice[1].type
    second_token = p.slice[2].type if len(p) > 2 else None

    if first_token == 'INTEGER':
        p[0] = p[1]
    elif first_token == '{':
        p[0] = p[2]

#    """expr : ID assign
#            | expr '.' ID '(' params ')'
#            | ID '(' params ')'
#            | IF expr THEN expr ELSE expr FI
#            | WHILE expr LOOP expr POOL
#            | '{' block '}'
#            | LET ID ':' TYPE assign_opt id_defs IN expr
#            | CASE expr OF typeactions ESAC
#            | NEW TYPE
#            | ISVOID expr
#            | expr '+' expr
#            | expr '-' expr
#            | expr '*' expr
#            | expr '/' expr
#            | INT_COMPLEMENT expr
#            | expr LESS expr
#            | expr LESSEQUAL expr
#            | expr EQUAL expr
#            | NOT expr
#            | '(' expr ')'
#            | ID
#            | INTEGER
#            | STRING
#            | BOOL"""
#    if len(p) == 2:
#        p[0] = p[1]
#    elif len(p) == 4:
#        if p[2] == '+':
#            p[0] = p[1] + p[3]
#        if p[2] == '-':
#            p[0] = p[1] - p[3]
#        if p[2] == '*':
#            p[0] = p[1] * p[3]
#        if p[2] == '/':
#            p[0] = p[1] / p[3]


#def p_params(p):
#    """params : expr
#              | expr ',' params"""

def p_block(p):
    """block : blockelements"""
    p[0] = Block(elements=p[1])

def p_blockelements(p):
    """blockelements : expr ';'
                  | expr ';' blockelements"""
    p[0] = (p[1],)
    if len(p) == 4:
        p[0] += p[3]

#def p_typeactions(p):
#    """typeactions : typeaction
#                   | typeaction typeactions"""
                   
#def p_typeaction(p):
#    """typeaction : ID ':' TYPE ACTION expr ';'"""

def p_empty(p):
    """empty :"""
    p[0] = None

def p_error(p):
    print('Syntax error in input at {!r}'.format(p))


# Create parser
yacc.yacc()

if __name__ == '__main__':

    import sys
    from pprint import pprint

    # Get file as argument

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

    pprint(t)
