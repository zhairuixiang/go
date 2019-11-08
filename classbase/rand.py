#!/bin/env python
# -*- coding: UTF-8 -*-

import random

class RandomGenerator1:
	@staticmethod
	def generate(count=10, start=1, stop=100):
		return [ random.randint(start, stop) for _ in range(count) ]	

#print(RandomGenerator1.generate(20, 100, 1000))

class RandomGenerator2:
	def __init__(self, start=1, stop=100):
		self.start = start
		self.stop = stop

	def generate(self, count=10):
		self.count = count
		return [ random.randint(self.start, self.stop) for _ in range(self.count) ]

#rg = RandomGenerator2(100, 200)
#print(rg.generate(20))

class RandomGenerator3:
	def __init__(self, start=1, stop=100):
		self.start = start
		self.stop = stop
		self._gen = self._generate()

	def _generate(self):
		while True:
			yield [ random.randint(self.start, self.stop) for _ in range(self.count) ]

	def generate(self, count=10):
		self.count = count
		return next(self._gen)

#rg = RandomGenerator3(1000, 10000)
#print(rg.generate(20))

class RandomGenerator4:
	def __init__(self, start=1, stop=100):
		self.start = start
		self.stop = stop
		self._gen = self._generate()

	def _generate(self):
		while True:
			yield random.randint(self.start, self.stop)

	def generate(self, count=10):
		self.count = count
		return [ next(self._gen) for _ in range(self.count) ]

#rg = RandomGenerator4(200, 300)
#print(rg.generate(20))

class RandomGenerator5:
	def __init__(self, start=1, stop=100):
		self.start = start
		self.stop = stop

	def generate(self, count=10):
		self.count = count
		return [ random.randint(self.start, self.stop) for _ in range(self.count) ]

	@property
	def num(self):
		return self.count

	@num.setter
	def num(self, val):
		self.count = val

#rg = RandomGenerator5(200, 5000)
#print(rg.generate(200))
