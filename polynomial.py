class Polynomial(object):
	"""polynomials in one variable x"""
	def __init__(self, *coeff):
		super(Polynomial, self).__init__()
		self.coeff = coeff

	def __repr__(self):
		s = ""
		for deg, c in enumerate(self.coeff):
			if deg == 0:
				s += str(c)
				if len(self.coeff) == 1:
					return "Polynomial: " + s
				else:
					continue
			if c == 0:
				continue
			elif c == 1:
				s += " + "
			elif c == -1:
				s += " - "
			elif c < 0:
				s += " - " + str(-c)
			elif c > 0:
				s += " + " + str(c)
			s += "x"
			if deg != 1:
				s += "^" + str(deg)
		return "Polynomial: " + s

	def degree(self):
		return len(self.coeff) - 1

	def __call__(self, num):
		res = 0
		for deg, coeff in enumerate(self.coeff):
			res += coeff * num**deg
		return res

	def __neg__(self):
		return Polynomial(*[-c for c in self.coeff])

	def __add__(self, other):
		if not isinstance(other, Polynomial):
			result = list(self.coeff)
			result[0] += other
		else:
			result = [a + b for a, b in zip(self.coeff, other.coeff)]
		return Polynomial(*result)

	def __radd__(self, other):
		return self.__add__(other)

	def __sub__(self, other):
		return self + -other

	def __rsub__(self, other):
		return -self.__sub__(other)

	def __mul__(self, other):
		if not isinstance(other, Polynomial):
			return Polynomial(*[other * c for c in self.coeff])
		n = self.degree() * other.degree() + 2
		result = [0] * (n)
		for i in range(n):
			for j in range(i+1):
				try:
					result[i] += self.coeff[j] * other.coeff[i - j]
				except IndexError as e:
					pass
		return Polynomial(*result)

	def __rmul__(self, other):
		return self.__mul__(other)

	def __pow__(self, other):
		if isinstance(other, Polynomial):
			raise TypeError("Polynomial exponents are not supported")
		else:
			if other == 1:
				return self
			elif other % 2 == 0:
				return (self*self)**(other // 2)
			else:
				return self * (self*self)**((other - 1) // 2)