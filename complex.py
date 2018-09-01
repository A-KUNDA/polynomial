"""
Class for complex numbers
"""

class Complex_Number(object):

	def __init__(self, real, imag=0):
		self.real = real
		self.imag = imag

	def __repr__(self):
		return str(self.real) + " + " + str(self.imag) + "i"

	def __add__(self, other):
		a = self.real + other.real
		b = self.imag + other.imag
		return Complex_Number(a, b)

	def __sub__(self, other):
		a = self.real - other.real
		b = self.imag - other.imag
		return Complex_Number(a, b)

	def __mul__(self, other):
		a = self.real*other.real - self.imag*other.imag
		b = self.real*other.imag + self.imag*other.real
		return Complex_Number(a, b)

	def __truediv__(self, other):
		z = self * other.conj()
		a = z.real / other.norm()
		b = z.imag / other.norm()
		return Complex_Number(a, b)

	def norm(self):
		return self.real**2 + self.imag**2

	def conj(self):
		return Complex_Number(self.real, -self.imag)