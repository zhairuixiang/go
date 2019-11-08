#!/bin/env python
# -*- coding: UTF-8 -*-

from collections import defaultdict
import re

def makekey2(line:str, chars=set("""!'"#./\()[],*- \r\n""")):
	start = 0

	for i,c in enumerate(line):
		if c in chars:
			if start == i: # 如果紧挨着还是特殊字符，start一定等于i
				start += i # 加1并continue
				continue
			yield line[start:i]
			start = i + 1 # 加1是跳过这个不需要的特殊字符c
	else:
		if start < len(line): # 小于，说明还有有效的字符，而且一直到末尾
			yield line[start:]

regex = re.compile('[^\w-]+')

def makekey3(line:str):
	for word in regex.split(line):
		if len(word):
			yield word

def wordcount(filename, encoding='utf8', ignore=set()):
	d = defaultdict(lambda:0)
	with open(filename, encoding=encoding) as f:
		for line in f:
			for word in map(str.lower, makekey2(line)):
				if word not in ignore:
					d[word] += 1
	return d

def top(d:dict, n=10):
	for i,(k,v) in enumerate(sorted(d.items(), key=lambda item: item[1], reverse=True)):
		if i > n:
			break
		print(k,v)

top(wordcount('sample.txt', ignore={'the', 'a'}))
