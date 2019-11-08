#!/bin/env python
# -*- coding: UTF-8 -*-

class Dispatcher:
	
	def register(self, cmd):
		def _register(func):
			if not isinstance(cmd, str):
				raise TypeError('{} is not str'.format(cmd))
			setattr(self.__class__, cmd, func)
		return _register

	def __call__(self, cmd):
		def _register(func):
			if not isinstance(cmd, str):
				raise TypeError('{} is not str'.format(cmd))
			setattr(self.__class__, cmd, func)
		return _register

	def run(self):
		while True:
			cmd = input("Please enter a command: ").strip()
			if cmd == 'quit':
				return
			else:
				print(getattr(self, cmd, self.defaultfunc)())

	def defaultfunc(self):
		return 'defaultfunc'

dis = Dispatcher()

@dis.register('python')
def python(self):
	return 'hello python'

@dis.register('java')
def java(self):
	return 'hello java'

@dis.register('php')
def php(self):
	return 'hello php'

@dis.register('perl')
def perl(self):
	return 'hello perl'

#dis.registry('python', lambda self: 'hello python')
#dis.registry('java', lambda self: 'hello java')

dis.run()
