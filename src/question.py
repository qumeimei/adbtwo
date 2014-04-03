import json
import urllib
from pprint import pprint
from util import *


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

class Question:
	
	def __init__(self, api_key):
		self.api_key = api_key
	
	def run(self, query, single = True):
		if single:
			print 'Let me see...'
		else:
			print 'Query-Question: ' + query
		
		# answer question
		print '\n\n'
		#api_key = open('.api_key').read()
		question=query.strip()

		query1=question.strip()
		query1 = ' '.join(question.split()[2:])
		suffix="?"
		if query1.endswith(suffix) == True:
			query1 = query1[:-1]
			bus_dict=dict()
			que=Question(self.api_key)
			dict1=que.mqlread(bus_dict,query1,CONFINE[0],CONFINE[1])
			dict2=que.mqlread(dict1,query1,CONFINE[2],CONFINE[3])
	
		x=1
		sl=101
		str=que.pl(sl,1)
		str +='	|'+' '*((sl-len(question))/2)+question+' '*((sl-len(question))/2)+' |'+'\n'
		str +=que.pl(sl,1)
	
		for key in sorted(dict2.iterkeys()):
		
			key1 = ' '.join(key.split()[0:len(key.split())-3])
			typ = ' '.join(key.split()[len(key.split())-2:len(key.split())-1])
			typ = typ[:-1]
			str+=que.prt(key1,'As','Creation')
			y=1
			str+='	|'+que.stl(20,81)
			for num in dict2[key]:
				if y==1:
					str+=que.prt(' ',typ,num)
				else:
					str+=que.prt(' ',' ',num)
				if y==len(dict2[key]):
					str +=que.pl(sl,1)
				y+=1
		print str
	
		x=1
		'''for key in sorted(dict2.iterkeys()):
			str=key
			z=1
			for num in dict2[key]:
				if z==len(dict2[key]) and z>1:
					str+= ', and '+'<'+num+'> '
				else:
					if z>1:
						str+= ', <'+num+'>'
					else:
						str+= '<'+num+'>'
				z+=1
			print "%d"  %(x)+'. ' +str
			x+=1
			'''


	def mqlread(self, bus_dict,key_word,confine_word,confine):
	
		service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
		query = [{confine_word: [{'a:name': None,'name~=': key_word}],'id': None,'name': None,'type': confine}]
		params = {
		'query': json.dumps(query),
		'key': self.api_key
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
	def pl(self,lenthofline,num_tab):
		return '	 '*num_tab+formatLine("-"*lenthofline, lenthofline, single = True)+'\n'
	def stl(self,before,after):
		return ' '*before+formatLine("-"*after, after, single = True)+'\n'
	def prt(self,nu1,nu2,nu3):
		return  '	|'+formatLine(' '+nu1, 20, single = True)+'|'+formatLine(nu2, 39, single = True)+'| '+formatLine(nu3, 39, single = True)+'|'+'\n'
