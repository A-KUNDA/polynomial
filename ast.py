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

class VarMexp(Mexp):
	"""
	Class for variables
	"""
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "VarMexp(" + name ")"

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

class AssignStatement(Equality):
	"""
	Class for assignments
	"""
	def __init__(self, name, mexp):
		self.name = name
		self.mexp = mexp
