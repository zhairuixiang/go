#!/bin/env python
# -*- coding: UTF-8 -*-

f = 'functions'

def countword(src):
	chars = '''~!@#$%^&*()_+{}[]|\\/"'=;:.-<>,'''

	with open(src, encoding='utf-8') as f:
		word_count = {}
		for line in f:
			words = line.split()

			for k,v in zip(words, (1,)*len(words)):
				k = k.strip(chars)
				k = k.lower()
				word_count[k] = word_count.get(k, 0) + 1
	
	lst = sorted(word_count.items(), key=lambda item: item[1], reverse=True)

	for i in range(10): print(lst[i])

	return lst

countword(f)
