#!/bin/env python
# -*- coding: UTF-8 -*-

from collections import OrderedDict
from urllib import request
import json

url = 'http://172.19.1.50/healthcheck/status?format=csv'

def tengineUpstreamCheck(url):
    response = request.urlopen(url)
    all_upstream = response.readlines()
    ret = {}
    ret['data'] = []

    for index in range(len(all_upstream)):
        upstream_dict = OrderedDict()
        upstream = all_upstream[index].decode()
        upstream_dict['{#UPSTREAM}'] = upstream.split(',')[1]
        upstream_dict['{#NAME}'] = upstream.split(',')[2]
        upstream_dict['{#STATUS}'] = upstream.split(',')[3]
        ret['data'].append(upstream_dict)

    return json.dumps(ret, indent=4)

result = tengineUpstreamCheck(url)

print(result)
