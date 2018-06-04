class Polynomial(object):
	"""polynomials in one variable x"""
	def __init__(self, *coeff):
		super(Polynomial, self).__init__()
		self.coeff = coeff

	def __repr__(self):
		s = ""
		for deg, c in enumerate(self.coeff):
			if c != 1:
				s += str(c)
			s += "x" + "^" + str(deg)
			if deg != len(self.coeff) - 1:
				s += " + "
		return "Polynomial: " + s

	def degree(self):
		return len(self.coeff) - 1

	def __call__(self, num):
		res = 0
		for deg, coeff in enumerate(self.coeff):
			res += coeff * num**deg
		return res

	def __add__(self, other):
		coeff1 = self.coeff
		coeff2 = other.coeff
		result = [a + b for a, b in zip(coeff1, coeff2)]
		return Polynomial(*result)

	def __sub__(self, other):
		coeff1 = self.coeff
		coeff2 = other.coeff
		result = [a - b for a, b in zip(coeff1, coeff2)]
		return Polynomial(*result)

f = Polynomial(1, 1, 41)
g = Polynomial(1, 2, 3)
print(f(2))