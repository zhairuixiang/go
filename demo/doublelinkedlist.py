#!/bin/env python
# -*- coding: UTF-8 -*-
# Version: 2.0
# Datetime: 2019-11-05
# Description: 链表数据结构实现

import copy
from collections import Iterable

class DoubleNode:
	def __init__(self, item, prev=None, next=None):
		"""初始化一个双向链表节点"""
		self.item = item
		self.prev = prev
		self.next = next

	def __repr__(self):
		"""格式化打印"""
		return '{} <== {} ==> {}'.format(self.prev.item if self.prev else self.prev,
										 self.item,
										 self.next.item if self.next else self.next)
	__str__ = __repr__


class DoubleLinkedList:
	def __init__(self, iterable=None, head=None, tail=None):
		"""初始化一个双向链表"""
		self.head = head
		self.tail = tail
		self.length = 0
		if iterable is not None:
			if isinstance(iterable, Iterable):
				for item in iterable:
					self.append(item)
			else:
				raise TypeError('{} object is not iterable'.format(type(iterable).__name__))

	@property
	def is_empty(self):
		"""判断链表是否为空"""
		return self.head is None

	def __len__(self):
		"""链表长度"""
		return self.length

	def __bool__(self):
		"""空链表返回False"""
		return False if len(self) is 0 else True

	def __getitem__(self, index):
		"""获取一个值"""
		return self.getitem(index)

	def __setitem__(self, index, value):
		"""设置一个值"""
		node = self.getitem(index)
		node.item = value

	def __iter__(self):
		"""返回一个迭代器"""
		return self.iternodes()

	def __contains__(self, item):
		"""判断元素是否在链表中"""
		for node in self:
			if item == node.item:
				return True
		else:
			return False

	def __add__(self, other):
		"""链表相加"""
		if not isinstance(other, type(self)):
			raise TypeError('can only concatenate {0} (not "{1}") to {0}'.format(type(self).__name__, type(other).__name__))
		newlinkedlist = copy.deepcopy(self)
		for node in other:
			newlinkedlist.append(node.item)
		return newlinkedlist

	def __iadd__(self, iterable):
		"""加等"""
		if not isinstance(iterable, Iterable):
			raise TypeError('{} object is not iterable'.format(type(iterable).__name__))
		if iterable is self:
			iterable = copy.deepcopy(iterable)
		for node in iterable:
			self.append(node.item if isinstance(iterable, type(self)) else node)
		return self

	def __mul__(self, integer):
		"""乘法"""
		if not isinstance(integer, int):
			raise TypeError("can't multiply sequence by non-int of type '{}'".format(type(other).__name__))
		if integer <= 0:
			return type(self)()
		newlinkedlist = type(self)()
		for _ in range(integer):
			for node in self:
				newlinkedlist.append(node.item)
		return newlinkedlist

	def __imul__(self, integer):
		"""乘等"""
		if not isinstance(integer, int):
			raise TypeError("can't multiply sequence by non-int of type '{}'".format(type(other).__name__))
		if integer <= 0:
			self.clear()
			return self
		newlinkedlist = copy.deepcopy(self)
		for _ in range(integer-1):
			for node in newlinkedlist:
				self.append(node.item)
		else:
			return self

	__hash__ = None

	def add(self, item):
		"""链表头部增加一个节点"""
		node = DoubleNode(item)
		if self.is_empty:
			self.tail = node
		else:
			self.head.prev = node
			node.next = self.head
		self.head = node
		self.length += 1
		
	def append(self, item):
		"""链表尾部追加一个节点"""
		node = DoubleNode(item)
		if self.is_empty:
			self.head = node
		else:
			self.tail.next = node
			node.prev = self.tail
		self.tail = node
		self.length += 1

	def extend(self, iterable):
		"""可迭代对象的元素来扩展列表"""
		if not isinstance(iterable, Iterable):
			raise TypeError('{} object is not iterable'.format(type(iterable).__name__))
		for obj in iterable:
			self.append(obj)

	def reverse(self):
		"""链表反转"""
		if self.is_empty or len(self) is 1:
			return
		current = self.head
		while current:
			next = current.next
			current.prev, current.next = current.next, current.prev
			current = next
		else:
			self.head, self.tail = self.tail, self.head
			
	def iternodes(self, reverse=False):
		"""迭代链表所有元素, 返回一个生成器对象"""
		current = self.tail if reverse else self.head
		while current:
			yield current
			current = current.prev if reverse else current.next

	def getitem(self, index):
		"""查找索引对应的值, 如果存在则返回, 否则抛出异常"""
		if not isinstance(index, int):
			raise TypeError('{} indices must be integers, not {}'.format(type(self).__name__, type(index).__name__))

		flag = 1 if index < 0 else 0
		for i,node in enumerate(self.iternodes(flag), flag):
			if abs(index) == i:
				return node
		else:
			raise IndexError('{} index out of range'.format(type(self).__name__))

	def count(self, item):
		"""查找值在链表中出现的次数"""
		counter = 0
		for node in self:
			if item == node.item:
				counter += 1
		else:
			return counter

	def __del_node(self, node):
		"""删除一个节点"""
		prev = node.prev
		next = node.next
		if prev is None and next is None:
			self.head = None
			self.tail = None
		elif prev is None:
			self.head = next
			next.prev = None
		elif next is None:
			self.tail = prev
			prev.next = None
		else:
			prev.next = next
			next.prev = prev

	def pop(self, index=None):
		"""删除并返回索引处的节点(默认为尾部)"""
		if self.is_empty:
			raise IndexError('empty {}'.format(type(self).__name__))

		if index is None:
			current = self.tail
			prev = current.prev
			if prev is None:
				self.head = None
				self.tail = None
			else:
				prev.next = None
				self.tail = prev
		else:
			current = self.getitem(index)
			self.__del_node(current)
		self.length -= 1
		return current.item

	def insert(self, index, item):
		"""在索引位置插入一个节点"""
		try:
			current = self.getitem(index)
		except IndexError:
			self.append(item)
			return

		newnode = DoubleNode(item)
		prev = current.prev
		if prev is None:
			self.head = newnode
		else:
			prev.next = newnode
			newnode.prev = prev
		newnode.next = current
		current.prev = newnode
		self.length += 1

	def remove(self, item):
		"""删除第一次出现的值"""
		for node in self:
			if item == node.item:
				current = node
				break
		else:
			raise ValueError('{} not in {}'.format(item, type(self).__name__))
		self.__del_node(current)
		self.length -= 1

	def clear(self):
		"""清空链表"""
		if not self.is_empty:
			for node in self:
				del node
			self.head = None
			self.tail = None
			self.length = 0

ll = DoubleLinkedList()
ll.add('java')
ll.add('ruby')
ll.add('python')
ll.append('php')
ll.append('perl')
ll.extend(['c', 'c++', 'c#'])
#for obj in ll: print(obj)
print('~'*30)

ll2 = DoubleLinkedList(['python', 'java', 'php'])
ll3 = DoubleLinkedList(['c', 'c#'])
ll2 *= -1
for obj in ll2: print(obj)
print(len(ll2))
#print('~'*30)
#for obj in newll: print(obj)
