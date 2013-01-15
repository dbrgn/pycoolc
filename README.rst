pycoolc
=======

.. image:: https://secure.travis-ci.org/dbrgn/pycoolc.png?branch=master
    :alt: Build status
    :target: http://travis-ci.org/dbrgn/pycoolc

A `cool`_ compiler written in Python 3 using `PLY`_.

Cool reference manual: `http://s.dbrgn.ch/4JrI <http://s.dbrgn.ch/4JrI>`__ (PDF).


Project status
--------------

Already implemented:

* Lexer
* Parser
* AST generation

Not yet done:

* Code generation
* Optimizations


Usage
-----

Run lexer::

    python3 -m pycoolc.lexer path/to/sourcefile.cl

Run parser::

    python3 -m pycoolc.parser path/to/sourcefile.cl

Use parser in your code:

.. sourcecode:: python

    >>> from pycoolc.parser import yacc
    >>> yacc.parse('class Main {};')
    (Type(name='Main', inherits=None, features=()),)


AST
---

The abstract syntax tree is composed of ``tuple``\ s and ``namedtuple``\ s.  As
an example, parsing ``example/complex2.cl`` currently results in an AST like
this:

.. sourcecode:: python

    (
      Type(
        name='Silly'
        inherits=None
        features=(
          Method(
            name='copy'
            type='SELF_TYPE'
            formals=()
            expr='self'
          )
        )
      )
      Type(
        name='Sally'
        inherits='Silly'
        features=()
      )
      Type(
        name='Main'
        inherits=None
        features=(
          Attribute(
            name='x'
            type='Sally'
            expr=MethodCall(
              object=New(
                type='Sally'
              )
              method='copy'
              params=()
            )
          )
          Attribute(
            name='y'
            type='Int'
            expr=BinaryOperation(
              operator='-'
              left=12
              right=9
            )
          )
          Attribute(
            name='z'
            type='Int'
            expr=If(
              condition=BinaryOperation(
                operator='<='
                left='y'
                right=42
              )
              true=BinaryOperation(
                operator='+'
                left=BinaryOperation(
                  operator='*'
                  left=5
                  right=3
                )
                right=2
              )
              false=0
            )
          )
          Method(
            name='main'
            type='Sally'
            formals=()
            expr='x'
          )
        )
      )
    )


Testing
-------

Make sure you have installed nose::

    pip install nose

Then just run the nose on the tests directory::

    nosetests tests


License
-------

License: GPLv3, see ``LICENSE`` file.



.. _cool: http://theory.stanford.edu/~aiken/software/cool/cool.html
.. _ply: http://www.dabeaz.com/ply/ 
