"""
Abstract Syntax Tree
"""

from equality import *

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