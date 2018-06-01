class Polynomial(object):
	"""polynomials in one variable x"""
	def __init__(self, *coeff):
		super(Polynomial, self).__init__()
		self.coeff = coeff

	def __repr__(self):
		s = ""
		for deg, c in enumerate(self.coeff):
			s += str(c) + "x" + "^" + str(deg)
			if deg != len(self.coeff) - 1:
				s += " + "
		return "Polynomial: " + s

	def degree(self):
		return len(self.coeff) - 1

	def eval(self, num):
		res = 0
		for deg, coeff in enumerate(self.coeff):
			res += coeff * num**deg
		return res

f = Polynomial(1, 1, 41)
print(f)