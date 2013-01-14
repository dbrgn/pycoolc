from nose.tools import assert_equal
from pycoolc.parser import yacc
from pycoolc import ast, utils

class TestProgram(object):
    """
    program ::= [[class;]]+
    """
    
    def test_single(self):
        src = """class Main {};"""
        out = yacc.parse(src)
        expected = (ast.Type(name='Main', inherits=None, features=()),)
        assert_equal(out, expected)

    def test_multiple(self):
        src = """
        class Ham { };
        class Spam { };
        class Main { };
        """
        out = yacc.parse(src)
        expected = (
            ast.Type(name='Ham', inherits=None, features=()),
            ast.Type(name='Spam', inherits=None, features=()),
            ast.Type(name='Main', inherits=None, features=()),
        )
        assert_equal(out, expected)
