pycoolc
=======

A `cool`_ compiler written in Python 3 using `PLY`_.

Development status: Alpha, not usable yet.

License: GPLv3.

Usage
-----

Run lexer::

    python3 -m pycoolc.lexer path/to/sourcefile.cl

Run parser::

    python3 -m pycoolc.parser path/to/sourcefile.cl

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

.. _cool: http://theory.stanford.edu/~aiken/software/cool/cool.html
.. _ply: http://www.dabeaz.com/ply/ 
