"""
Abstract Syntax Tree
"""

from equality import *
from parser import *

class Mexp(Equality):
	"""
	Class for mathematical expressions
	"""
	pass

class IntMexp(Mexp):
	"""
	Class for numbers
	"""
	def __init__(self, i):
		self.i = i

	def __repr__(self):
		return "IntMexp(" + str(self.i) + ")"

	def eval(self, env):
		return self.i

class VarMexp(Mexp):
	"""
	Class for variables
	"""
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "VarMexp(" + name ")"

	def eval(self, env):
		if self.name in env:
			return env[self.name]
		else:
			return 0

class BinopMexp(Mexp):
	"""
	Class for binary operations
	"""
	def __init__(self, op, left, right):
		self.op = op
		self.left = left
		self.right = right

	def __repr__(self):
		return "BinopMexp(" + self.op + ", " + self.left + ", " + self.right ")"

	def eval(self, env):
		left_value = self.left.eval(env)
		right_value = self.right.eval(env)
		if self.op == "+":
			value = left_value + right_value
		elif self.op == "-":
			value = left_value - right_value
		elif self.op == "*":
			value = left_value * right_value
		elif self.op == "/":
			value = left_value / right_value
		else:
			raise RuntimeError("Unknown operator: " + self.op)
		return value

class AssignStatement(Equality):
	"""
	Class for assignments
	"""
	def __init__(self, name, mexp):
		self.name = name
		self.mexp = mexp

	def eval(self, env):
		value = self.mexp.eval(env)
		env[self.name] = value

def keyword(kw):
	return Reserved(kw, RESERVED)

iD = Tag(ID)
num = Tag(NUM) ^ (lambda i: int(i))

def mexp_value():
	return (num ^ (lambda i: IntMexp(i))) | (iD ^ (lambda v: VarMexp(v)))

def process_group(parsed):
	((_, p), _) = parsed
	return p

def mexp_group():
	return keyword("(") + Lazy(mexp) + keyword(")") ^ process_group

def mexp_term():
	return mexp_value() | mexp_group()

def process_binop(op):
	return lambda l, r: BinopMexp(op, l, r)

def any_operator_in_list(ops):
	op_parsers = [keyword(op) for op in ops]
	parser = reduce(lambda l, r: l | r, op_parsers)
	return parser

mexp_precedence_levels = [["*", "/"], ["+", "-"]]

def precedence(value_parser, precedence_levels, combine):
	def op_parser(precedence_level):
		return any_operator_in_list(precedence_level) ^ combine
	parser = value_parser * op_parser(precedence_levels[0])
	for precedence_level in precedence_levels[1:]:
		parser = parser * op_parser(precedence_level)
	return parser

def mexp():
	return precedence(mexp_term(), mexp_precedence_levels, process_binop)