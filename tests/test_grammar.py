"""
This module contains tests for the cool grammar as defined by the `The Cool
Reference Manual <http://s.dbrgn.ch/4JrI>`__.
"""
from nose.tools import assert_equal, assert_is
from pycoolc.parser import *


def get_parser(start):
    """Return a customized parser."""
    return yacc.yacc(start=start, errorlog=yacc.NullLogger()).parse


class TestProgram:
    """
    program ::= [[ class; ]]+
    """

    def setUp(self):
        self.parse = get_parser('program')

    def test_single(self):
        src = 'class Main {};'
        out = self.parse(src)
        expected = (ast.Type(name='Main', inherits=None, features=()),)
        assert_equal(out, expected)

    def test_multiple(self):
        src = 'class Ham { }; class Spam { }; class Main { };'
        out = self.parse(src)
        expected = (
            ast.Type(name='Ham', inherits=None, features=()),
            ast.Type(name='Spam', inherits=None, features=()),
            ast.Type(name='Main', inherits=None, features=()),
        )
        assert_equal(out, expected)


class TestClass:
    """
    class ::= class TYPE [ inherits TYPE ] { [[ feature; ]]* }
    """

    def setUp(self):
        self.parse = get_parser('class')

    def test_simple(self):
        src = 'class Spam { };'
        out = self.parse(src)
        expected = ast.Type(name='Spam', inherits=None, features=())
        assert_equal(out, expected)

    def test_inheritance(self):
        src = 'class Spam inherits Ham { };'
        out = self.parse(src)
        expected = ast.Type(name='Spam', inherits='Ham', features=())
        assert_equal(out, expected)

    def test_feature(self):
        src = 'class Spam { nine : Int; };'
        out = self.parse(src)
        expected = ast.Type(
            name='Spam', inherits=None, features=(
                ast.Attribute(name=ast.Ident('nine'), type='Int', expr=None),
            )
        )
        assert_equal(out, expected)

    def test_features(self):
        src = 'class Spam { nine : Int; name : Str; };'
        out = self.parse(src)
        expected = ast.Type(
            name='Spam', inherits=None, features=(
                ast.Attribute(name=ast.Ident('nine'), type='Int', expr=None),
                ast.Attribute(name=ast.Ident('name'), type='Str', expr=None),
            )
        )
        assert_equal(out, expected)


class TestFeature:
    """
    feature ::= ID( [ formal [[ , formal ]]* ] ) : TYPE { expr }
            ::= ID : TYPE [ <- expr ]
    """

    def setUp(self):
        self.parse = get_parser('feature')

    def test_attribute_simple(self):
        src = 'spam : Ham;'
        out = yacc.parse(src)
        expected = ast.Attribute(name=ast.Ident('spam'), type='Ham', expr=None)
        assert_equal(out, expected)

    def test_attribute_expr(self):
        src = 'spam : Ham <- "bacon";'
        out = yacc.parse(src)
        expected = ast.Attribute(name=ast.Ident('spam'), type='Ham', expr="bacon")
        assert_equal(out, expected)

    def test_method_simple(self):
        src = 'spam() : Ham { 42 };'
        out = yacc.parse(src)
        expected = ast.Method(name=ast.Ident('spam'), type='Ham', formals=(), expr=42)
        assert_equal(out, expected)

    def test_method_formal(self):
        src = 'spam(bacon : Egg) : Ham { 42 };'
        out = yacc.parse(src)
        expected = ast.Method(name=ast.Ident('spam'), type='Ham', expr=42, formals=(
            ast.Formal(name=ast.Ident('bacon'), type='Egg'),
        ))
        assert_equal(out, expected)

    def test_method_formals(self):
        src = 'spam(bacon : Egg, sausage : Meat) : Ham { 42 };'
        out = yacc.parse(src)
        expected = ast.Method(name=ast.Ident('spam'), type='Ham', expr=42, formals=(
            ast.Formal(name=ast.Ident('bacon'), type='Egg'),
            ast.Formal(name=ast.Ident('sausage'), type='Meat'),
        ))
        assert_equal(out, expected)


class TestFormal:
    """
    formal ::= ID : TYPE
    """

    def setUp(self):
        self.parse = get_parser('formal')

    def test(self):
        src = 'spam : Ham'
        out = yacc.parse(src)
        expected = ast.Formal(name=ast.Ident('spam'), type='Ham')
        assert_equal(out, expected)


class TestExpression:
    """
    expr ::= ID <- expr
         ::= expr[@TYPE].ID( [ expr [[ , expr ]]* ] )
         ::= ID( [ expr [[ , expr ]]* ] )
         ::= if expr then expr else expr fi
         ::= while expr loop expr pool
         ::= { [[ expr; ]]+ }
         ::= let ID : TYPE [ <- expr ] [[ , ID : TYPE [ <- expr ] ]]* in expr
         ::= case expr of [[ ID : TYPE => exp; ]]+ esac
         ::= new TYPE
         ::= isvoid expr
         ::= expr + expr
         ::= expr - expr
         ::= expr * expr
         ::= expr / expr
         ::= ~expr
         ::= expr < expr
         ::= expr <= expr
         ::= expr = expr
         ::= not expr
         ::= (expr)
         ::= ID
         ::= integer
         ::= string
         ::= true
         ::= false
    """

    def setUp(self):
        self.parse = get_parser('expr')

    def test_assignment(self):
        src = 'bacon <- "eggs"'
        out = yacc.parse(src)
        expected = ast.Assignment(name=ast.Ident('bacon'), expr='eggs')
        assert_equal(out, expected)

    def test_method_call_simple(self):
        src = 'pub.show_vikings()'
        out = yacc.parse(src)
        expected = ast.MethodCall(object=ast.Ident('pub'), targettype=None,
            method=ast.FunctionCall(
                name=ast.Ident('show_vikings'), params=()
            )
        )
        assert_equal(out, expected)

    def test_method_call_arg(self):
        src = 'pub.show_vikings(42)'
        out = yacc.parse(src)
        expected = ast.MethodCall(object=ast.Ident('pub'), targettype=None,
            method=ast.FunctionCall(
                name=ast.Ident('show_vikings'), params=(42,)
            )
        )
        assert_equal(out, expected)

    def test_method_call_args(self):
        src = 'pub.show_vikings(42, "spam")'
        out = yacc.parse(src)
        expected = ast.MethodCall(object=ast.Ident('pub'), targettype=None,
            method=ast.FunctionCall(
                name=ast.Ident('show_vikings'), params=(42, 'spam')
            )
        )
        assert_equal(out, expected)

    def test_method_call_targettype(self):
        src = 'pub@Place.has_spam()'
        out = yacc.parse(src)
        expected = ast.MethodCall(object=ast.Ident('pub'), targettype='Place',
            method=ast.FunctionCall(
                name=ast.Ident('has_spam'), params=()
            )
        )
        assert_equal(out, expected)

    def test_function_call_simple(self):
        src = 'order_spam()'
        out = yacc.parse(src)
        expected = method=ast.FunctionCall(name=ast.Ident('order_spam'), params=())
        assert_equal(out, expected)

    def test_function_call_arg(self):
        src = 'order_spam(42)'
        out = yacc.parse(src)
        expected = method=ast.FunctionCall(name=ast.Ident('order_spam'), params=(42,))
        assert_equal(out, expected)

    def test_function_call_args(self):
        src = 'order_spam(42, "spam")'
        out = yacc.parse(src)
        expected = method=ast.FunctionCall(name=ast.Ident('order_spam'), params=(42, "spam"))
        assert_equal(out, expected)

    def test_if(self):
        src = 'if true then 42 else 23 fi'
        out = yacc.parse(src)
        expected = ast.If(condition=True, true=42, false=23)
        assert_equal(out, expected)

    def test_while(self):
        src = 'while true loop "spam" pool'
        out = yacc.parse(src)
        expected = ast.While(condition=True, action='spam')
        assert_equal(out, expected)

    def test_block(self):
        src = '{ 1; "bacon"; 3; }'
        out = yacc.parse(src)
        expected = ast.Block(elements=(1, 'bacon', 3))
        assert_equal(out, expected)

    def test_let_basic(self):
        src = 'let x : Int in x'
        out = yacc.parse(src)
        expected = ast.Let(assignments=(
            ast.Attribute(name=ast.Ident('x'), type='Int', expr=None),
        ), expr=ast.Ident('x'))
        assert_equal(out, expected)

    def test_let_single(self):
        src = 'let x : Int <- 42 in x'
        out = yacc.parse(src)
        expected = ast.Let(assignments=(
            ast.Attribute(name=ast.Ident('x'), type='Int', expr=42),
        ), expr=ast.Ident('x'))
        assert_equal(out, expected)

    def test_let_multiple(self):
        src = 'let x : Int <- 42, y : Bool <- false in x'
        out = yacc.parse(src)
        expected = ast.Let(assignments=(
            ast.Attribute(name=ast.Ident('x'), type='Int', expr=42),
            ast.Attribute(name=ast.Ident('y'), type='Bool', expr=False),
        ), expr=ast.Ident('x'))
        assert_equal(out, expected)

    def test_case_single(self):
        src = 'case "spam" of x : Str => true; esac'
        out = yacc.parse(src)
        expected = ast.Case(expr='spam', typeactions=(
            ast.TypeAction(name=ast.Ident('x'), type='Str', expr=True),
        ))
        assert_equal(out, expected)

    def test_case_multiple(self):
        src = 'case "spam" of x : Str => true; y : Object => false; esac'
        out = yacc.parse(src)
        expected = ast.Case(expr='spam', typeactions=(
            ast.TypeAction(name=ast.Ident('x'), type='Str', expr=True),
            ast.TypeAction(name=ast.Ident('y'), type='Object', expr=False),
        ))
        assert_equal(out, expected)

    def test_new(self):
        src = 'new Bacon'
        out = yacc.parse(src)
        expected = ast.New(type='Bacon')
        assert_equal(out, expected)

    def test_isvoid(self):
        src = 'isvoid viking'
        out = yacc.parse(src)
        expected = ast.UnaryOperation(operator='isvoid', right=ast.Ident('viking'))
        assert_equal(out, expected)
    
    def test_plus(self):
        src = '"hi" + " there"'
        out = yacc.parse(src)
        expected = ast.BinaryOperation(operator='+', left='hi', right=' there')
        assert_equal(out, expected)

    def test_minus(self):
        src = '44 - 2'
        out = yacc.parse(src)
        expected = ast.BinaryOperation(operator='-', left=44, right=2)
        assert_equal(out, expected)

    def test_times(self):
        src = '21 * 2'
        out = yacc.parse(src)
        expected = ast.BinaryOperation(operator='*', left=21, right=2)
        assert_equal(out, expected)

    def test_divided(self):
        src = '84 / 2'
        out = yacc.parse(src)
        expected = ast.BinaryOperation(operator='/', left=84, right=2)
        assert_equal(out, expected)

    def test_int_complement(self):
        src = '~42'
        out = yacc.parse(src)
        expected = ast.UnaryOperation(operator='~', right=42)
        assert_equal(out, expected)

    def test_less(self):
        src = '40 < 42'
        out = yacc.parse(src)
        expected = ast.BinaryOperation(operator='<', left=40, right=42)
        assert_equal(out, expected)

    def test_less_or_equal(self):
        src = '42 <= fourtytwo'
        out = yacc.parse(src)
        expected = ast.BinaryOperation(operator='<=', left=42, right=ast.Ident('fourtytwo'))
        assert_equal(out, expected)

    def test_equal(self):
        src = '4 = 2'
        out = yacc.parse(src)
        expected = ast.BinaryOperation(operator='=', left=4, right=2)
        assert_equal(out, expected)

    def test_not(self):
        src = 'not true'
        out = yacc.parse(src)
        expected = ast.UnaryOperation(operator='not', right=True)
        assert_equal(out, expected)

    def test_parens(self):
        src = '(30 + 12)'
        out = yacc.parse(src)
        expected = ast.BinaryOperation(operator='+', left=30, right=12)
        assert_equal(out, expected)

    def test_id(self):
        src = 'my_ham'
        out = yacc.parse(src)
        expected = ast.Ident('my_ham')
        assert_equal(out, expected)

    def test_integer(self):
        src = '42'
        out = yacc.parse(src)
        assert_equal(out, 42)

    def test_string(self):
        src = '"spam"'
        out = yacc.parse(src)
        assert_equal(out, 'spam')

    def test_true(self):
        src = 'true'
        out = yacc.parse(src)
        assert_is(out, True)

    def test_false(self):
        src = 'false'
        out = yacc.parse(src)
        assert_is(out, False)
