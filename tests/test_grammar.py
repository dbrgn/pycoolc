"""
This module contains tests for the cool grammar as defined by the `The Cool
Reference Manual <http://s.dbrgn.ch/4JrI>`__.
"""
from nose.tools import assert_equal
from pycoolc.parser import *


def get_parser(start):
    """Return a customized parser."""
    return yacc.yacc(start=start, errorlog=yacc.NullLogger()).parse


class TestProgram:
    """
    program ::= [[class;]]+
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
    class ::= class TYPE [inherits TYPE] { [[feature;]]* }
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
                ast.Attribute(name='nine', type='Int', expr=None),
            )
        )
        assert_equal(out, expected)

    def test_features(self):
        src = 'class Spam { nine : Int; name : Str; };'
        out = self.parse(src)
        expected = ast.Type(
            name='Spam', inherits=None, features=(
                ast.Attribute(name='nine', type='Int', expr=None),
                ast.Attribute(name='name', type='Str', expr=None),
            )
        )
        assert_equal(out, expected)


class TestFeature:
    """
    feature ::= ID( [ formal [[, formal]]* ] ) : TYPE { expr }
            ::= ID : TYPE [<- expr]
    """

    def setUp(self):
        self.parse = get_parser('feature')

    def test_attribute_simple(self):
        src = 'spam : Ham;'
        out = yacc.parse(src)
        expected = ast.Attribute(name='spam', type='Ham', expr=None)
        assert_equal(out, expected)

    def test_attribute_expr(self):
        src = 'spam : Ham <- "bacon";'
        out = yacc.parse(src)
        expected = ast.Attribute(name='spam', type='Ham', expr="bacon")
        assert_equal(out, expected)

    def test_method_simple(self):
        src = 'spam() : Ham { 42 };'
        out = yacc.parse(src)
        expected = ast.Method(name='spam', type='Ham', formals=(), expr=42)
        assert_equal(out, expected)

    def test_method_formal(self):
        src = 'spam(bacon : Egg) : Ham { 42 };'
        out = yacc.parse(src)
        expected = ast.Method(name='spam', type='Ham', expr=42, formals=(
            ast.Formal(name='bacon', type='Egg'),
        ))
        assert_equal(out, expected)

    def test_method_formals(self):
        src = 'spam(bacon : Egg, sausage : Meat) : Ham { 42 };'
        out = yacc.parse(src)
        expected = ast.Method(name='spam', type='Ham', expr=42, formals=(
            ast.Formal(name='bacon', type='Egg'),
            ast.Formal(name='sausage', type='Meat'),
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
        expected = ast.Formal(name='spam', type='Ham')
        assert_equal(out, expected)
