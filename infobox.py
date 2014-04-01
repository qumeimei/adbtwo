#!/usr/bin/python
import json
import urllib
import sys
from entity_types import *

# global variables
FREEBASE = [
	'/people/person',
	'/book/author',
	'/film/actor',
	'/tv/tv_actor',
	'/organization/organization_founder',
	'/business/board_member',
	'/sports/sports_league',
	'/sports/sports_team',
	'/sports/professional_sports_team'
]
API_KEY = open(".api_key").read()

def search(query):
	service_url = 'https://www.googleapis.com/freebase/v1/search'
	params = {
		'query': query,
		'key': API_KEY
	}
	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())
	return [result['mid'] for result in response['result']]

def topic(topic_id):
	service_url = 'https://www.googleapis.com/freebase/v1/topic'
	params = {
		'key': API_KEY
	}
	url = service_url + topic_id + '?' + urllib.urlencode(params)
	return json.loads(urllib.urlopen(url).read())['property']

def filtertype(response):
	res = []
	for value in response['/type/object/type']['values']:
		if (value['id'] in FREEBASE) and (value['id'] not in res):
			res.append(value['id'])
	return res

def main():
	query = 'ac milan'
	mids = search(query.strip())
	if not mids:
		print 'No related information about query [' + query + '] was found!'
		sys.exit(0)
	response = []
	types = []
	for i, mid in enumerate(mids):
		response = topic(mid)
		types = filtertype(response)
		if types:
			break
		else:
			j = i + 1
			if j % 5 == 0:
				print j + ' Search API result entries were considered. None of them of a supported type.'
	if not types:
		print 'None of the Search API results of a supported type.'
		sys.exit(0)

	# retrieve and store information
	item = QueryItem(types, response)
	item.output()

	#f = open('topic6', 'w')
	#json.dump(response, f, indent=4)

main()
