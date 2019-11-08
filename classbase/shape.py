#!/bin/env python
# -*- coding: UTF-8 -*-

import math
import pickle
import json
import msgpack

class Shape:
	@property
	def area(self):
		raise NotImplementedError('基类未实现')

class Triangle(Shape):
	def __init__(self, bottom, weight):
		self.bottom = bottom
		self.weight = weight

	@property
	def area(self):
		return self.bottom * self.weight / 2

class Rectangle(Shape):
	def __init__(self, width, height):
		self.width = width
		self.height = height

	@property
	def area(self):
		return self.width * self.height

class SerializationMixin:
	def dumps(self, src, tp='pickle'):
		if tp == 'pickle':
			return pickle.dumps(src)
		elif tp == 'json':
			return json.dumps(src)
		elif tp == 'msgpack':
			return msgpack.dumps(src)
		else:
			raise TypeError('unknown serialization')

	def loads(self, src, tp='pickle'):
		if tp == 'pickle':
			return pickle.loads(src)
		elif tp == 'json':
			return json.loads(src)
		elif tp == 'msgpack':
			return msgpack.loads(src)
		else:
			raise TypeError('unknown deserialization')

class Circle(SerializationMixin, Shape):
	def __init__(self, radius):
		self.radius = radius
	
	@property
	def area(self):
		return math.pi * self.radius * self.radius

#t = Triangle(15, 10)
#print(t.area)

#r = Rectangle(10,5)
#print(r.area)

c = Circle(5.5)
print(c.__dict__)
