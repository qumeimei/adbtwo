import json
import urllib
from pprint import pprint

CONFINE = [
	'/book/author/works_written',
	'/book/author',
	'/organization/organization_founder/organizations_founded',
	'/organization/organization_founder'
]

IDENTITY = [
	' (as Author) created ',
	' (as Businessperson) created ',
]
api_key = open('.api_key').read()

def mqlread(bus_dict,key_word,confine_word,confine):
	service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
	query = [{confine_word: [{'a:name': None,'name~=': key_word}],'id': None,'name': None,'type': confine}]
	params = {
    'query': json.dumps(query),
    'key': api_key
	}
	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())
	
	if len (bus_dict)==0:
		modify=IDENTITY[0]
	else:
		modify=IDENTITY[1]

	for planet in response['result']:
		#print planet['name']
		for anb in planet[confine_word]:
			if planet['name']+modify in bus_dict.keys():
				bus_dict[planet['name']+modify].append(anb['a:name'])
			else:
				bus_dict[planet['name']+modify]=[anb['a:name']]
	return bus_dict

def main():
	question='who created Microsoft?'
	query=question.strip()
	query = ' '.join(question.split()[2:])
	suffix="?"
	if query.endswith(suffix) == True:
		query = query[:-1]
	print query
	bus_dict=dict()
	dict1=mqlread(bus_dict,query,CONFINE[0],CONFINE[1])
	dict2=mqlread(dict1,query,CONFINE[2],CONFINE[3])
	#pprint(dict2)
	
	x=1
	for key in sorted(dict2.iterkeys()):
		str=key
		y=1
		for num in dict2[key]:
			if y==len(dict2[key]) and y>1:
				str+= ', and '+'<'+num+'> '
			else:
				if y>1:
					str+= ', <'+num+'>'
				else:
					str+= '<'+num+'>'
			y+=1
		print "%d"  %(x)+'. ' +str
		x+=1
	
main()