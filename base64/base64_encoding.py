#!/bin/env python
# -*- coding: UTF-8 -*-

teststr = 'zrxabc'

def base64_encoding(src):
	'''base64 encoding'''
	def alphabet():
		ret = bytes()
		for start, end in ( (65,91), (97,123), (48,58) ):
			ret += bytes(range(start, end))
		else:
			ret += b'+/'
		return ret	

	def _base64(src):
		base64str = alphabet().decode()
		ret = ''
		src_length = len(src)
		for offset in range(0, src_length, 3):
			if offset+3 <= src_length:
				string = src[offset:offset+3]
			else:
				string = src[offset:]
			
			transbin = ''
			for char in string:
				charbin = bin(ord(char))[2:]
				length = len(charbin)
				transbin += '0' * (8 - length) + charbin
	
			len_transbin = len(transbin)
			for offset in range(0, len_transbin, 6):
				if offset+6 <= len_transbin:
					binstr = transbin[offset:offset+6]
				else:
					binstr = transbin[offset:] + '0' * (offset+6 - len_transbin)
				ret += base64str[int(binstr,2)]
		return ret
	
	def tail(src):
		tail = len(src) % 3
		if tail:
			tailstr = '=' * (2 if tail is 1 else 1)
			return tailstr
		else:
			return ''

	return (_base64(src) + tail(src)).encode()

print(base64_encoding(teststr))

import base64
print(base64.b64encode(teststr.encode()))
