#!/bin/env python
# -*- coding: UTF-8 -*-

from functools import partial

class StaticMethod:
	def __init__(self, mtd):
		self.mtd = mtd

	def __get__(self, instance, owner):
		return self.mtd

class ClassMethod:
	def __init__(self, mtd):
		self.mtd = mtd

	def __get__(self, instance, owner):
		return partial(self.mtd, owner)

class Person:
	def __init__(self, name, age):
		self.name = name
		self.age = age

	@StaticMethod  # => eat = StaticMethod(eat)
	def eat():
		return 'Person eat'

	@ClassMethod   # => say = ClassMethod(say)
	def say(cls):
		return 'Person say'

	@staticmethod
	def run():
		return 'Person run'


zhai = Person('zaizai', 18)
print(Person.run(), zhai.run())
print(Person.eat(), zhai.eat())
print(Person.say(), zhai.say())
