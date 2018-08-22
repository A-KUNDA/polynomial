RESERVED = "RESERVED"
NUM = "NUM"
ID = "ID"

class Result(object):
	
	def __init__(self, value, pos):
		self.value = value
		self.pos = pos

	def __repr__(self):
		return f"Result({self.value}, {self.pos})"

class Parser(object):

	def __call__(self, tokens, pos):
		return None

	def __add__(self, other):
		return Concat(self, other)

	def __mul__(self, other):
		return Exp(self, other)

	def __or__(self, other):
		return Alternate(self, other)

	def __xor__(self, fnc):
		return Process(self, fnc)

class Reserved(Parser):

	def __init__(self, value, tag):
		self.value = value
		self.tag = tag

	def __call__(self, tokens, pos):
		if pos < len(tokens) and \
		   tokens[pos][0] == self.value and \
		   tokens[pos][1] is self.tag:
			return Result(tokens[pos][0], pos + 1)
		else:
			return None

class Tag(Parser):

	def __init__(self, tag):
		self.tag = tag

	def __call__(self, tokens, pos):
		if pos < len(tokens) and tokens[pos][1] is self.tag:
			return Result(tokens[pos][0], pos + 1)
		else:
			return None

class Concat(Parser):

	def __init__(self, left, right):
		self.left = left
		self.right = right

	def __call__(self, tokens, pos):
		left_result = self.left(tokens, pos)
		if left_result:
			right_result = self.right(tokens, left_result.pos)
			if right_result:
				combined_value = (left_result.value, right_result.value)
				return Result(combined_value, right_result.pos)
		return None

class Exp(Parser):

	def __init__(self, parser, separator):
		self.parser = parser
		self.separator = separator

	def __call__(self, tokens, pos):
		result = self.parser(tokens, pos)

		def process_next(parsed):
			(sepfnc, right) = parsed
			return sepfnc(result.value, right)
		next_parser = self.separator + self.parser ^ process_next

		next_result = result
		while next_result:
			next_result = next_parser(tokens, result.pos)
			if next_result:
				result = next_result
		return result

class Alternate(Parser):

	def __init__(self, left, right):
		self.left = left
		self.right = right

	def __call__(self, tokens, pos):
		left_result = self.left(tokens, pos)
		if left_result:
			return left_result
		else:
			right_result = self.right(tokens, pos)
			return right_result

class Process(Parser):

	def __init__(self, parser, function):
		self.parser = parser
		self.function = function

	def __call__(self, tokens, pos):
		result = self.parser(tokens, pos)
		if result:
			result.value = self.function(result.value)
			return result

class Lazy(Parser):

	def __init__(self, parser_fnc):
		self.parser = None
		self.parser_fnc = parser_fnc

	def __call__(self, tokens, pos):
		if not self.parser:
			self.parser = self.parser_fnc()
		return self.parser(tokens, pos)

class Phrase(Parser):

	def __init__(self, parser):
		self.parser = parser

	def __call__(self, tokens, pos):
		result = self.parser(tokens, pos)
		if result and result.pos == len(tokens):
			return result
		else:
			return None

iD = Tag(ID)

# modify to handle complex numbers
num = Tag(NUM) ^ (lambda i: int(i) if float(i).is_integer() else float(i))