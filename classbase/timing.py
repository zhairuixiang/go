#!/bin/env pyhon
# -*- coding: UTF-8 -*-

import time
import datetime
from functools import wraps

def timing(func):
	@wraps(func)
	def _wrapper(*args, **kwargs):
		start = datetime.datetime.now()
		ret = func(*args, **kwargs)
		delta = (datetime.datetime.now() - start).total_seconds()
		print(delta)
		return ret

	return _wrapper

class Timing:
	def __init__(self, func):
		self.func = func
		wraps(func)(self)

	def __enter__(self):
		self.start = datetime.datetime.now()
		return self.func

	def __call__(self, *args, **kwargs):
		start = datetime.datetime.now()
		ret = self.func(*args, **kwargs)
		delta = (datetime.datetime.now() - start).total_seconds()
		print("{} took {}s".format(self.func.__name__, delta))
		return ret
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		print((datetime.datetime.now() - self.start).total_seconds())

#@timing
@Timing
def add(x, y):
	"""This is add function."""
	time.sleep(2)
	return x + y

print(add(4,5))
print(add.__doc__)
print(type(add), add.__dict__)

#with Timing(add) as func:
#	print(add(4,5))	
