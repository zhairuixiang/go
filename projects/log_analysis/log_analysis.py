#!/bin/bash
# -*- coding: UTF-8 -*-
# Version: 3.0
# Datetime: 2019-09-19
# Description: 日志分析

import re
import datetime
from queue import Queue
import threading
from types import FunctionType
from collections import Iterable
from pathlib import Path
from user_agents import parse
from collections import defaultdict
from functools import wraps
import inspect

def checktype(func):
	'''函数参数类型检查'''
	@wraps(func)
	def _checktype(*args, **kwargs):
		sig = inspect.signature(func)
		params = sig.parameters
		keys = list(params.keys())

		def _checkparams(k,v):
			'''检查参数类型'''
			annotation = params[k].annotation
			if annotation is not inspect._empty and not isinstance(v, annotation):
				raise ValueError('{} is not {}'.format(v, annotation))	

		for k,v in enumerate(args):
			k = keys[k]
			_checkparams(k,v)
			
		for k,v in kwargs.items():
			_checkparams(k,v)
				
		ret = func(*args, **kwargs)
		return ret
	return _checktype
##############################################################

f1 = 'logfile/test.log'
f2 = 'logfile/access.log'
logstr = '''42.120.74.236 - - [18/Apr/2017:11:03:05 +0800] "GET /index.php?m=cron HTTP/1.1" 200 31 "http://job.magedu.com/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"'''
ops = {
	'datetime': lambda timestr: datetime.datetime.strptime(timestr, '%d/%b/%Y:%H:%M:%S %z'),
	'status': int,
	'body_size': int,
	'http_user_agent': lambda useragent: parse(useragent)
}

@checktype
def extract(line:str) -> dict:
	'''
	:param line: 单行日志
	:return: dict
	'''
	pattern = '(?P<remote_addr>(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)) [^\s]+ [^\s]+ \[(?P<datetime>[^\[\]]+)\] "(?P<method>[^\s]+) (?P<uri>[^\s]+) (?P<protocol>[^"]+)" (?P<status>\d{3}) (?P<body_size>\d+) "(?P<referer>[^"]*)" "(?P<http_user_agent>[^"]+)"'
	regex = re.compile(pattern)
	matcher = regex.match(line)
	if matcher:
		return { k: ops.get(k, lambda x: x)(v) for k,v in matcher.groupdict().items() }
	else:
		raise Exception('No match', line)

@checktype
def openfile(filename:str):
	'''
	打开一个文件
	:param filename: 文件路径
	:return: generator
	'''
	with open(filename) as f:
		for line in f:
			yield extract(line)

@checktype
def load(*path:str): 
	'''
	:param path: 文件路径
	:return: generator
	'''
	for filename in path:
		filename = Path(filename)	
		if not filename.exists():
			continue	
		elif filename.is_dir():
			for file in filename.iterdir():
				if file.is_file():
					yield from openfile(str(file))
		elif filename.is_file():
			yield from openfile(str(filename))

#for i in load(f): print(i)

##################################################################
import random
import time
def source():
	'''模拟数据源'''
	while True:
		yield {
			'datetime': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))), 
			'number': random.randint(1,100)
		}
		time.sleep(1)


##################################################################
@checktype
def window(src:Queue, handler:FunctionType, width:int, interval:int, time_field:str='datetime'):
	'''
	:param src: 数据源
	:param handler: 处理数据的函数
	:param width: 查看数据的时间宽度
	:param interval: 处理数据的时间间隔
	:param time_field: 数据中的时间字段
	:return: None
	'''
	start = datetime.datetime.strptime('1970/01/01 00:00:00 +0800', '%Y/%m/%d %H:%M:%S %z')
	buffer = []
	delta = datetime.timedelta(seconds=width - interval)

	while True:
		data = src.get()

		buffer.append(data)
		current = data[time_field]

		if (current - start).total_seconds() >= interval:
			ret = handler(buffer)
			print(ret)
			start = current

			## buffer 处理
			buffer = [ data for data in buffer if data[time_field] > (current - delta) ]

def donothing_handler(iterable):
	print(list(map(lambda item: item['datetime'], iterable)))

@checktype
def status_handler(iterable:list) -> dict:
	'''状态码分析'''
	status = {}
	for element in iterable:
		key = element['status']
		if key not in status.keys():
			status[key] = 0
		status[key] += 1
	total = sum(status.values())
	return dict(map(lambda item: (item[0], '%{:.2f}'.format(item[1] / total * 100)), status.items()))
	#print({ k: v / total * 100 for k,v in status.items() })
		
@checktype
def browser_handler(iterable:list) -> dict:
	'''浏览器分析'''
	ua_dict = defaultdict(lambda :0)
	for item in iterable:
		ua = item['http_user_agent']
		key = (ua.browser.family, ua.browser.version_string)
		ua_dict[key] += 1

	return ua_dict
		

#window(load(f), donothing_handler, 3, 2, 'datetime')

##################################################################
@checktype
def dispatcher(src:Iterable) -> FunctionType:
	'''
	数据源分发到各个消费者处理
	:param src: 数据源(可迭代对象)
	:return: function
	'''
	queues = []
	threads = []

	def registry(handler, width, interval):
		'''函数注册'''
		queue = Queue()
		queues.append(queue)

		thread = threading.Thread(target=window, args=(queue, handler, width, interval))
		threads.append(thread)

	def run():
		'''启动'''
		for thread in threads:
			thread.start()

		for data in src:
			for queue in queues:
				queue.put(data)	

	return registry, run

registry, run = dispatcher(load(f1))

### 函数注册
#registry(donothing_handler, 3, 2)
registry(status_handler, 10, 5)
registry(browser_handler, 10, 10)

### 启动
run()
