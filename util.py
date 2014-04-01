#!/usr/bin/python
import json

def getContent(propmap, first, seconds = None, field = 'text'):
	res = []
	if first in propmap:
		for value in propmap[first]['values']:
			if propmap[first]['valuetype'] != 'compound':
				res.append(value[field])
			else:
				# keys must not be None
				tmp = []
				for key in seconds:
					tmp.append(getContent(value['property'], key))
				res.append(tmp)
	return res

