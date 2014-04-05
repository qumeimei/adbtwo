import json
import urllib
import sys
import re
from util import *

CONFINE = [
		'/book/author/works_written',
		'/book/author',
		'/organization/organization_founder/organizations_founded',
		'/organization/organization_founder'
]

IDENTITY = [
		' (as Author) created ',
		' (as Business_Person) created ',
]
sll=105
sl=sll-4
class Question:
	
	def __init__(self, api_key):
		self.api_key = api_key
	
	def run(self, query, single = True):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		query = query.strip()
		if single:
			print 'Let me see...'
		else:
			print '\nQuery-Question: ' + query
		
		if re.match('^who created .*', query.lower()) is None:
			print 'Wrong question!!! *_*\n'
			return
		
		question = query.strip(' |?')
		if len(question.split()) < 3:
			print 'Wrong question!!! *_*\n'
			return

		content = ' '.join(question.split()[2:])
		bus_dict=dict()
		dict1=self.mqlread(bus_dict,content,CONFINE[0],CONFINE[1])
		dict2=self.mqlread(dict1,content,CONFINE[2],CONFINE[3])
		
		question += '?'
		str=self.pl(sll,1)
		str +='	|'+' '*((sll-len(question))/2)+ question +' '*(sll-(sll-len(question))/2-len(question))+'|'+'\n'
		
		word_max=0
		names=[]
		for key in sorted(dict2.iterkeys()):
			key1 = ' '.join(key.split()[0:len(key.split())-3])
			word_max=max(word_max, len(key1))
			names.append(key1)
		#print "word_max is: %d " %(word_max)
		
		x=0
		for key in sorted(dict2.iterkeys()):
			key1 = ' '.join(key.split()[0:len(key.split())-3])
			typ = ' '.join(key.split()[len(key.split())-2:len(key.split())-1])
			typ = typ[:-1]
			
			if key1==names[x-1]:
				y=1
				for num in dict2[key]:
					if y==1:
						str+=self.prt(' ',typ,num,word_max,(sl-word_max)/2)
					else:
						str+=self.prt(' ',' ',num,word_max,(sl-word_max)/2)	
					y+=1
					
			else:
				str +=self.pl(sll,1)
				#
				str+=self.prt(key1,'As','Creation',word_max,(sl-word_max)/2)
				#
				str+='	|'+self.stl(word_max+2,sl-word_max+2)
				y=1
				for num in dict2[key]:
					if y==1:
						str+=self.prt(' ',typ,num,word_max,(sl-word_max)/2)
					else:
						str+=self.prt(' ',' ',num,word_max,(sl-word_max)/2)	
					y+=1
			
			x+=1
		str +=self.pl(sll,1)	
		print str.encode('utf-8')

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

	def prt(self,nu1,nu2,nu3,num4,num5):
		return  '	|'+formatLine(' '+nu1, num4+2, single = True)+ \
		'|'+formatLine(nu2, num5, single = True)+'|'+formatLine(nu3, sll-num5-num4-4, single = True)+'|'+'\n'
