#!/bin/env python
# -*- coding: UTF-8 -*-

class Temperature:
	def __init__(self, t, unit='c'):
		if unit == 'c':
			self._c = t
			self._f = self.c2f(t)
			self._k = self.c2k(t)
		elif unit == 'f':
			self._f = t
			self._c = self.f2c(t)
			self._k = self.f2k(t)
		elif unit == 'k':
			self._k = t
			self._c = self.k2c(t)
			self._f = self.k2f(t)
		else:
			raise TypeError('无法识别的类型{}'.format(unit))

	@property
	def c(self):
		return self._c
	
	@property
	def f(self):
		return self._f
	
	@property
	def k(self):
		return self._k

	@classmethod
	def c2f(cls, c):
		return 9 * c / 5 + 32

	@classmethod
	def f2c(cls, f):
		return 5 * (f - 32) / 9

	@classmethod
	def c2k(cls, c):
		return c + 273.15

	@classmethod
	def k2c(cls, k):
		return k - 273.15

	@classmethod
	def f2k(cls, f):
		c = cls.f2c(f)
		return cls.c2k(c)

	@classmethod
	def k2f(cls, k):
		c = cls.k2c(k)
		return cls.c2f(c)

#print(Temperature.c2f(30))
#print(Temperature.c2k(30))

#print(Temperature.f2c(86))
#print(Temperature.f2k(86))

#print(Temperature.k2c(303.15))
#print(Temperature.k2f(303.15))

tmp = Temperature(30, 'c')
print(tmp.c, tmp.f, tmp.k)
