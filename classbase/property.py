#!/bin/env python
# -*- coding: UTF-8 -*-

class Property:
	def __init__(self, fget=None, fset=None, fdel=None):
		self.fget = fget
		self.fset = fset
		self.fdel = fdel

	def __get__(self, instance, owner):
		if instance is not None:
			return self.fget(instance)
		return self

	def __set__(self, instance, value):
		if self.fset is None:
			raise AttributeError("can't set attribute")
		self.fset(instance, value)

	def __delete__(self, instance):
		pass

	def setter(self, fset):
		return type(self)(self.fget, fset, self.fdel)

class Person:
	def __init__(self, name, age=0):
		self._name = name
		self.__age = age

	@Property # => age = property(age)
	def age(self):
		return self.__age

	@age.setter  # => age = age.setter(age)
	def age(self, value):
		self.__age = value

zhai = Person('zaizai', 18)
print(zhai.age)
print(Person.age)
zhai.age = 20
print(zhai.age)
Person.age = 30
