"""
Abstract Syntax Tree
"""
import operator
from functools import reduce
from parse import *
from polynomial import Polynomial

class Mexp(object):
	"""
	Class for mathematical expressions
	"""
	pass

class IntMexp(Mexp):
	"""
	Class for numbers
	"""
	def __init__(self, i, sign="+"):
		if sign == "-":
			self.i = -i
		elif sign == "+":
			self.i = i

	def __repr__(self):
		return f"IntMexp({self.i})"

	def eval(self, env):
		return self.i

class VarMexp(Mexp):
	"""
	Class for variables
	"""
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return f"VarMexp({self.name})"

	def eval(self, env):
		if self.name in env:
			return env[self.name]
		else:
			return Polynomial(0, 1)

class UnopMexp(Mexp):
	"""
	Class for unary operations on the left
	+, -
	"""
	def __init__(self, op, operand):
		self.op = op
		self.operand = operand

	def __repr(self):
		return f"UnopMexp({self.op}, {self.operand})"

	def eval(self, env):
		right_value = self.right.eval(env)
		if self.op == "-":
			value = - right_value
		elif self.op == "+":
			value = right_value
		else:
			raise RuntimeError(f"Unknown operator: {self.op}")
		return value

class BinopMexp(Mexp):
	"""
	Class for binary operations
	+, -, *, /, ^
	"""
	binops = {
		"+": operator.add,
		"-": operator.sub,
		"*": operator.mul,
		"/": operator.truediv,
		"^": operator.pow,
		".": lambda l, r: float(str(l) + "." + str(r))
		}

	def __init__(self, op, left, right):
		self.op = op
		self.left = left
		self.right = right

	def __repr__(self):
		return f"BinopMexp({self.op}, {self.left}, {self.right})"

	def eval(self, env):
		left_value = self.left.eval(env)
		right_value = self.right.eval(env)
		if self.op in self.binops:
			value = self.binops[self.op](left_value, right_value)
		else:
			raise RuntimeError(f"Unknown operator: {self.op}")
		return value

class AssignStatement(object):
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

def mexp_value():
	return (num ^ (lambda i: IntMexp(i))) | (iD ^ (lambda v: VarMexp(v)))

def process_group(parsed):
	((_, p), _) = parsed
	return p

def mexp_group():
	return keyword("(") + Lazy(mexp) + keyword(")") ^ process_group

def mexp_term():
	return mexp_value() | mexp_group()

def process_unop(op):
	return lambda x: UnopMexp(op, x)

def process_binop(op):
	return lambda l, r: BinopMexp(op, l, r)

def process_op(op):
	if op == "-":
		return process_unop(op)()
	else:
		return process_binop(op)()

def any_operator_in_list(ops):
	op_parsers = [keyword(op) for op in ops]
	parser = reduce(lambda l, r: l | r, op_parsers)
	return parser

mexp_precedence_levels = [["."], ["^"], ["*", "/"], ["+", "-"]]

def precedence(value_parser, precedence_levels, combine):
	def op_parser(precedence_level):
		return any_operator_in_list(precedence_level) ^ combine
	parser = value_parser * op_parser(precedence_levels[0])
	for precedence_level in precedence_levels[1:]:
		parser = parser * op_parser(precedence_level)
	return parser

def mexp():
	return precedence(mexp_term(), mexp_precedence_levels, process_binop)

def assign_stmt():
	def process(parsed):
		((name, _), exp) = parsed
		return AssignStatement(name, exp)
	return iD + keyword("=") + mexp ^ process

def stmt():
	return assign_stmt()

def stmt_list():
	separator = keyword(";") ^ (lambda x: lambda l, r: l * r)
	return Exp(stmt(), separator)

def parser():
	return Phrase(stmt_list())

def parse(tokens):
	#ast = parser()(tokens, 0)
	ast = mexp()(tokens, 0)
	return ast