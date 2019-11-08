#!/bin/env python
# -*- coding: UTF-8 -*-

import inspect
from functools import wraps

def checktype(func):
	@wraps(func)
	def _checktype(*args, **kwargs):
		sig = inspect.signature(func)
		params = sig.parameters
		keys = list(params.keys())

		def _checkparams(k):
			annotation = params[k].annotation
			if annotation is not inspect._empty and not isinstance(v, annotation):
				raise TypeError('{} is not {}'.format(v, annotation.__name__))

		for i,v in enumerate(args):
			k = keys[i]
			_checkparams(k)

		for k,v in kwargs.items():
			_checkparams(k)

		return func(*args, **kwargs)
	return _checktype

class Typed:
	def __init__(self, name, type):
		self.name = name
		self.type = type

	def __get__(self, instance, owner):
		if instance is not None:
			return instance.__dict__[self.name]
		return self

	def __set__(self, instance, value):
		if not isinstance(value, self.type):
			raise TypeError('{} is not {}'.format(value, self.type.__name__))
		instance.__dict__[self.name] = value

def typeassert(cls):
	params = inspect.signature(cls).parameters
	print(params)
	for name,param in params.items():
		print(param.name, param.annotation)
		if param.annotation != param.empty:
			setattr(cls, name, Typed(name, param.annotation))
	return cls

@typeassert
class Person:
	#name = Typed('name', str)
	#age = Typed('age', int)

	def __init__(self, name:str, age:int):
		self.name = name
		self.age = age

zhai = Person('zaizai', 18)
print(zhai.name, zhai.age)
print(zhai.__dict__)
print(type(zhai).__dict__)
