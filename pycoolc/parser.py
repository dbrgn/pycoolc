from collections import namedtuple
import ply.yacc as yacc
from . import lexer
tokens = lexer.tokens

# AST namedtuples

Type = namedtuple('Type', 'name inherits features')
Method = namedtuple('Method', 'name type formals expr')
Block = namedtuple('Block', 'elements')
Attribute = namedtuple('Attribute', 'name type expr')
Let = namedtuple('Let', 'assignments expr')
If = namedtuple('If', 'condition true false')
Case = namedtuple('Case', 'name type action')
Assignment = namedtuple('Assignment', 'name expr')
Formal = namedtuple('Formal', 'name type')
New = namedtuple('New', 'type')
MethodCall = namedtuple('MethodCall', 'object method params')
FunctionCall = namedtuple('FunctionCall', 'function params')
BinaryOperation = namedtuple('BinaryOperation', 'operator left right')
UnaryOperation = namedtuple('UnaryOperation', 'operator right')

# Grammar definitions in BNF form

precedence = (
    ('right', 'ASSIGN'),
    ('right', 'NOT'),
    ('nonassoc', 'LESSEQUAL', 'LESS', 'EQUAL'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'ISVOID'),
    ('right', 'INT_COMPLEMENT'),
    #('right', '@'),
    ('left', '.'),
)

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
    p[0] = Type(name=p[2], inherits=p[3], features=p[5])

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
    p[0] = Attribute(name=p[1], type=p[3], expr=p[4])

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
    else:
        raise SyntaxError('Invalid number of symbols')

def p_formal(p):
    """formal : ID ':' TYPE"""
    p[0] = Formal(name=p[1], type=p[3])

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
        p[0] = (p[1],)
    elif len(p) == 4:
        p[0] = (p[1],) + p[3]
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

def p_typeactions(p):
    """typeactions : typeaction
                   | typeaction typeactions"""
    if len(p) == 2:
        p[0] == (p[1],)
    elif len(p) == 3:
        p[0] = (p[1],) + p[2]
    else:
        raise SyntaxError('Invalid number of symbols')
                   
def p_typeaction(p):
    """typeaction : ID ':' TYPE ACTION expr ';'"""
    p[0] = Case(name=p[1], type=p[3], action=p[5])

def p_expr(p):
    """expr : ID assign
            | expr '.' ID '(' params_opt ')'
            | ID '(' params_opt ')'
            | IF expr THEN expr ELSE expr FI
            | WHILE expr LOOP expr POOL
            | LET attr_defs IN expr
            | CASE expr OF typeactions ESAC
            | NEW TYPE
            | INT_COMPLEMENT expr
            | NOT expr
            | ISVOID expr
            | expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
            | expr LESS expr
            | expr LESSEQUAL expr
            | expr EQUAL expr
            | '{' block '}'
            | '(' expr ')'
            | ID
            | INTEGER
            | STRING
            | BOOL
    """
    # todo LET and second expr
    first_token = p.slice[1].type
    second_token = p.slice[2].type if len(p) > 2 else None
    third_token = p.slice[3].type if len(p) > 3 else None

    if first_token == 'ID':
        if second_token is None:
            p[0] = p[1]
        elif second_token == '(':
            p[0] = FunctionCall(function=p[1], params=p[3])
        elif second_token == 'assign':
            p[0] = Assignment(name=p[1], expr=p[2])
    elif first_token == 'expr':
        if len(p) == 4 and third_token == 'expr':
            p[0] = BinaryOperation(operator=p[2], left=p[1], right=p[3])
        elif second_token == '.':
            p[0] = MethodCall(object=p[1], method=p[3], params=p[5])
    elif first_token == 'IF':
        p[0] = If(condition=p[2], true=p[4], false=p[6])
    elif first_token == 'LET':
        p[0] = Let(assignments=p[2], expr=p[4])
    elif first_token == 'NEW':
        p[0] = New(type=p[2])
    elif first_token in ['ISVOID', 'INT_COMPLEMENT', 'NOT']:
        p[0] = UnaryOperation(operator=p[1], right=p[2])
    elif first_token in ['{', '(']:
        p[0] = p[2]
    elif first_token in ['INTEGER', 'STRING', 'BOOL']:
        p[0] = p[1]

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
