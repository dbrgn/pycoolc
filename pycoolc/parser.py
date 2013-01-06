from collections import namedtuple
import ply.yacc as yacc
from . import lexer
tokens = lexer.tokens

# AST namedtuples

Class = namedtuple('Class', 'name inherits features')
Method = namedtuple('Method', 'name type formals expr')
Block = namedtuple('Block', 'elements')
VariableCreation = namedtuple('VariableCreation', 'name type expr')
Let = namedtuple('Let', 'variables expr')
Assignment = namedtuple('Assignment', 'name expr')
Formal = namedtuple('Formal', 'name type')
New = namedtuple('New', 'type')
MethodCall = namedtuple('MethodCall', 'object method params')

# Grammar definitions in BNF form

def p_program(p):
    """program : classes"""
    p[0] = p[1]

def p_classes(p):
    """classes : class
               | class classes"""
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 3:
        p[0] = (p[1],) + p[2]
    else:
        raise SyntaxError('Invalid number of symbols')

def p_class(p):
    """class : CLASS TYPE inheritance '{' features_opt '}' ';'"""
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

def p_features_opt(p):
    """features_opt : features
                    | empty"""
    if p.slice[1].type == 'empty':
        p[0] = tuple()
    else:
        p[0] = p[1]

def p_features(p):
    """features : feature
                | feature features"""
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 3:
        p[0] = (p[1],) + p[2]
    else:
        raise SyntaxError('Invalid number of symbols')
    
def p_feature(p):
    """feature : ID '(' formals_opt ')' ':' TYPE '{' expr '}' ';'
               | attr_def ';'"""
    if len(p) == 11:
        p[0] = Method(name=p[1], type=p[6], formals=p[3], expr=p[8])
    elif len(p) == 3:
        p[0] = p[1]
    else:
        raise SyntaxError('Invalid number of symbols')

def p_attr_defs(p):
    """attr_defs : attr_def
                 | attr_def ',' attr_defs"""
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 4:
        p[0] = (p[1],) + p[3]
    else:
        raise SyntaxError('Invalid number of symbols')

def p_attr_def(p):
    """attr_def : ID ':' TYPE assign_opt"""
    p[0] = VariableCreation(name=p[1], type=p[3], expr=p[4])

def p_assign_opt(p):
    """assign_opt : assign
                  | empty"""
    p[0] = p[1]

def p_assign(p):
    """assign : ASSIGN expr"""
    p[0] = p[2]

def p_formals_opt(p):
    """formals_opt : formals
                   | empty"""
    if p.slice[1].type == 'empty':
        p[0] = tuple()
    else:
        p[0] = p[1]

def p_formals(p):
    """formals : formal
               | formal ',' formals"""
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 4:
        p[0] = (p[1],) + p[3]

def p_formal(p):
    """formal : ID ':' TYPE"""
    p[0] = Formal(name=p[1], type=p[3]) 

def p_expr(p):
    """expr : ID assign
            | expr '.' ID '(' params_opt ')'
            | LET ID ':' TYPE assign_opt attr_defs IN expr
            | NEW TYPE
            | '{' block '}'
            | '(' expr ')'
            | ID
            | INTEGER
    """
    first_token = p.slice[1].type
    second_token = p.slice[2].type if len(p) > 2 else None

    if first_token == 'ID':
        if second_token is None:
            p[0] = p[1]
        elif second_token == 'assign':
            p[0] = Assignment(name=p[1], expr=p[2])
    elif first_token == 'expr':
        if second_token == '.':
            p[0] = MethodCall(object=p[1], method=p[3], params=p[5])
    elif first_token == 'LET':
        p[0] = Let(variables=p[6], expr=p[8])
    elif first_token == 'NEW':
        p[0] = New(type=p[2])
    elif first_token in ['{', '(']:
        p[0] = p[2]
    elif first_token in ['INTEGER', 'STRING', 'BOOL']:
        p[0] = p[1]

#    """expr # ID assign
#            # expr '.' ID '(' params_opt ')'
#            | ID '(' params_opt ')'
#            | IF expr THEN expr ELSE expr FI
#            | WHILE expr LOOP expr POOL
#            | '{' block '}'
#            # LET ID ':' TYPE assign_opt attr_defs IN expr
#            | CASE expr OF typeactions ESAC
#            # NEW TYPE
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
#            # '(' expr ')'
#            # ID
#            # INTEGER
#            # STRING
#            # BOOL"""
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


def p_params_opt(p):
    """params_opt : params
                  | empty"""
    if p.slice[1].type == 'empty':
        p[0] = tuple()
    else:
        p[0] = p[1]

def p_params(p):
    """params : expr
              | expr ',' params"""
    if len(p) == 2:
        p[0] = (p[2],)
    elif len(p) == 4:
        p[0] = (p[2],) + p[4]
    else:
        raise SyntaxError('Invalid number of symbols')

def p_block(p):
    """block : blockelements"""
    p[0] = Block(elements=p[1])

def p_blockelements(p):
    """blockelements : expr ';'
                     | expr ';' blockelements"""
    if len(p) == 3:
        p[0] = (p[1],)
    elif len(p) == 4:
        p[0] = (p[1],) + p[3]
    else:
        raise SyntaxError('Invalid number of symbols')

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
