#!/bin/env python
# -*- coding: UTF-8 -*-

teststr = 'enJ4YWJj'

def base64_decoding(src):
	
	def alphabet():
		ret = bytes()
		for start, end in ( (65,91), (97,123), (48,58) ):
			ret += bytes(range(start, end))
		else:
			ret += b'+/'
		return ret
	
	def decoding(src):
		base64str = alphabet().decode()
		src_length = len(src)
		ret = ''

		for offset in range(0, src_length, 4):
			string = src[offset:offset+4]
			
			transbin = ''
			for char in string:
				if char is '=': continue
				charbin = bin(base64str.find(char))[2:]
				length = len(charbin)
				transbin += '0' * (6 - length) + charbin
			#print(transbin, len(transbin))

			len_transbin = len(transbin)
			for offset in range(0, len_transbin, 8):
				if offset+8 <= len_transbin:
					binstr = transbin[offset:offset+8]
				else:
					binstr = transbin[offset:] + '0' * (offset+8 - len_transbin)
				ret += chr(int(binstr,2))
				#print(chr(int(binstr,2)))
		return ret
	
	return decoding(src)

result = base64_decoding(teststr)
print(result)

import base64
print(base64.b64decode(teststr).decode())
