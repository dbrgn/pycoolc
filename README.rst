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
an example, parsing ``example/compley.cl`` currently results in code like this:

.. sourcecode:: python

    (
        Type(
            name='Silly',
            inherits=None,
            features=(
                Method(
                    name='copy',
                    type='SELF_TYPE',
                    params=(),
                    expr='self'
                ),
            )
        ),

        Type(
            name='Sally',
            inherits='Silly',
            features=()
        ),

        Type(
            name='Main',
            inherits=None,
            features=(
                Attribute(
                    name='x',
                    type='Sally',
                    expr=MethodCall(
                        object=New(
                            type='Sally'
                        ),
                        method='copy',
                        params=()
                    )
                ),
                Method(
                    name='main',
                    type='Sally',
                    params=(),
                    expr='x'
                )
            )
        )
    )

.. _cool: http://theory.stanford.edu/~aiken/software/cool/cool.html
.. _ply: http://www.dabeaz.com/ply/ 
