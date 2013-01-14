from collections import namedtuple


Assignment = namedtuple('Assignment', 'name expr')
Attribute = namedtuple('Attribute', 'name type expr')
BinaryOperation = namedtuple('BinaryOperation', 'operator left right')
Block = namedtuple('Block', 'elements')
Case = namedtuple('Case', 'name type action')
Formal = namedtuple('Formal', 'name type')
FunctionCall = namedtuple('FunctionCall', 'function params')
If = namedtuple('If', 'condition true false')
Let = namedtuple('Let', 'assignments expr')
MethodCall = namedtuple('MethodCall', 'object method params')
Method = namedtuple('Method', 'name type formals expr')
New = namedtuple('New', 'type')
Type = namedtuple('Type', 'name inherits features')
UnaryOperation = namedtuple('UnaryOperation', 'operator right')
