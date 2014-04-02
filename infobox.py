#!/usr/bin/python
import json
import urllib
import sys

# map freebase type to project type
FREEBASEMAP = {
	'/people/person': 'PERSON',
	'/book/author': 'AUTHOR',
	'/film/actor': 'ACTOR',
	'/tv/tv_actor': 'ACTOR',
	'/organization/organization_founder': 'BUSINESS_PERSON',
	'/business/board_member': 'BUSINESS_PERSON',
	'/sports/sports_league': 'LEAGUE',
	'/sports/sports_team': 'SPORTS_TEAM',
	'/sports/professional_sports_team': 'SPORTS_TEAM'
}

# utility function to retrieve information from the freebase results
def getContent(propmap, first, seconds = None, field = 'text'):
	res = []

	if first in propmap:	
		for value in propmap[first]['values']:
			if propmap[first]['valuetype'] != 'compound':
				res.append(value[field])
			
			else:
				# keys must not be None
				tmp = []
				empty = True
				for key in seconds:
					tc = getContent(value['property'], key)
					empty = empty and not tc
					tmp.append(tc)

				# check if tmp = [[], [], ... ] then not add in res
				if not empty:
					res.append(tmp)
	
	return res

# debug function
def dump(x):
	print '#' * 100
	print x
	print '#' * 100

# wrap a query result with a class
class QueryItem:
	def __init__(self, types, response):
		self.res = response
		self.result = {}

		# order of item types
		self.typeOrder = {
			'PERSON': 1, 'AUTHOR': 2, 'ACTOR': 3, 'BUSINESS_PERSON': 4, 'LEAGUE': 5, 'SPORTS_TEAM': 6
		}

		# order of attributes of each type
		self.attrOrder = {
			'PERSON': {
				'Name': 1, 'Birthday': 2, 'Place of birth': 3, 'Death': 4, 'Siblings': 5, 'Spouses': 6, 'Description': 7
			},
			'AUTHOR': {
				'Books': 1, 'Influenced By': 2, 'Books about': 3, 'Influenced': 4
			},
			'ACTOR': {
				'Films' : 1
			},
			'BUSINESS_PERSON': {
				'Leadership': 1, 'Board Member': 2, 'Founded': 3
			},
			'LEAGUE': {
				'Name': 1, 'Sport': 2, 'Slogan': 3, 'Official Website': 4, 'Championship': 5, 'Teams': 6, 'Description': 7
			},
			'SPORTS_TEAM': {
				'Name': 1, 'Sport': 2, 'Arena': 3, 'Championships': 4, 'Founded': 5, 'Leagues': 6, 'Locations': 7,
				'Coaches': 8, 'PlayersRoster': 9, 'Description': 10
			}
		}

		flag1 = True
		flag2 = True
		flag3 = True
		for atype in types:
			if FREEBASEMAP[atype] == 'PERSON':
				self.__setPerson()
				continue
			if FREEBASEMAP[atype] == 'AUTHOR':
				self.__setAuthor()
				continue
			if FREEBASEMAP[atype] == 'ACTOR' and flag1:
				self.__setActor()
				flag1 = False
				continue
			if FREEBASEMAP[atype] == 'BUSINESS_PERSON' and flag2:
				self.__setBusinessPerson()
				flag2 = False
				continue
			if FREEBASEMAP[atype] == 'LEAGUE':
				self.__setLeague()
				continue
			if FREEBASEMAP[atype] == 'SPORTS_TEAM' and flag3:
				self.__setSportsTeam()
				flag3 = False

	# common properties
	def __setName(self, itype):
		self.result[itype]['Name'] = ', '.join(getContent(self.res, '/type/object/name'))
		self.name = self.result[itype]['Name']

	def __setDes(self, itype):
		des = getContent(self.res, '/common/topic/description', None, 'value')
		self.result[itype]['Description'] = des[0] if des else ''

	# Person properties
	def __setPerson(self):
		itype = 'PERSON'
		self.result[itype] = {}

		# name and description
		self.__setName(itype)
		self.__setDes(itype)

		# birthday and place of birth
		self.result[itype]['Birthday'] = ', '.join(getContent(self.res, '/people/person/date_of_birth'))
		self.result[itype]['Place of birth'] = ', '.join(getContent(self.res, '/people/person/place_of_birth'))
	
		# death
		place = ' '.join(getContent(self.res, '/people/deceased_person/place_of_death'))
		date = ' '.join(getContent(self.res, '/people/deceased_person/date_of_death'))
		cause = ', '.join(getContent(self.res, '/people/deceased_person/cause_of_death'))
		tmp = ''
		if date:
			tmp += date + ' '
		if place:
			tmp += 'at ' + place
		if cause:
			tmp += ', cause: (' + cause + ')'
		self.result[itype]['Death'] = tmp.strip() 

		# siblings
		tmp = []
		for sib in getContent(self.res, '/people/person/sibling_s', ['/people/sibling_relationship/sibling']):
			tmp.append(sib[0][0])
		self.result[itype]['Siblings'] = tmp

		# spouses
		spouses = []
		info = getContent(self.res, '/people/person/spouse_s', \
			['/people/marriage/spouse', '/people/marriage/from', '/people/marriage/to', '/people/marriage/location_of_ceremony'])
		for sp in info:
			tmp = ''
			name = sp[0][0] if sp[0] else ''
			ff = sp[1][0] if sp[1] else ''
			ft = sp[2][0] if sp[2] else ''
			place = sp[3][0] if sp[3] else ''
			if name:
				tmp += name
			if ff:
				tmp += ' (' + ff + ' - '
				if ft:
					tmp += ft
				else:
					tmp += 'now'
				tmp += ')'
			if place:
				tmp += ' @ ' + place
			spouses.append(tmp)
		self.result[itype]['Spouses'] = spouses

	# Author properties
	def __setAuthor(self):
		itype = 'AUTHOR'
		self.result[itype] = {}
		
		# books, books about, influenced, and influenced by
		self.result[itype]['Books'] = getContent(self.res, '/book/author/works_written')
		self.result[itype]['Books about'] = getContent(self.res, '/book/book_subject/works')
		self.result[itype]['Influenced'] = getContent(self.res, '/influence/influence_node/influenced')
		self.result[itype]['Influenced By'] = getContent(self.res, '/influence/influence_node/influenced_by')

	# Actor properties
	def __setActor(self):
		itype = 'ACTOR'
		self.result[itype] = {}
		self.result[itype]['Films'] = getContent(self.res, '/film/actor/film', ['/film/performance/film', '/film/performance/character'])
	
	# Business Person properties
	def __setBusinessPerson(self):
		itype = 'BUSINESS_PERSON'
		self.result[itype] = {}

		# founded companies, leadership, and board member
		self.result[itype]['Founded'] = getContent(self.res, '/organization/organization_founder/organizations_founded')
		self.result[itype]['Leadership'] =  getContent(self.res, '/business/board_member/leader_of', \
			['/organization/leadership/organization', '/organization/leadership/role', '/organization/leadership/title', \
			'/organization/leadership/from', '/organization/leadership/to'])
		self.result[itype]['Board Member'] = getContent(self.res, '/business/board_member/organization_board_memberships', \
			['/organization/organization_board_membership/organization', '/organization/organization_board_membership/role', \
			'/organization/organization_board_membership/title', '/organization/organization_board_membership/from', \
			'/organization/organization_board_membership/to'])

	# League properties
	def __setLeague(self):
		itype = 'LEAGUE'
		self.result[itype] = {}

		# name and description
		self.__setName(itype)
		self.__setDes(itype)

		# sport, slogan, championship, website
		self.result[itype]['Sport'] = ', '.join(getContent(self.res, '/sports/sports_league/sport'))
		self.result[itype]['Slogan'] = '. '.join(getContent(self.res, '/organization/organization/slogan'))
		self.result[itype]['Championship'] = ', '.join(getContent(self.res, '/sports/sports_league/championship'))
		self.result[itype]['Official Website'] = ', '.join(getContent(self.res, '/common/topic/official_website'))

		# teams
		tmp = []
		for team in getContent(self.res, '/sports/sports_league/teams', ['/sports/sports_league_participation/team']):
			tmp.append(team[0][0])
		self.result[itype]['Teams'] = tmp

	# Sports Team properties
	def __setSportsTeam(self):
		itype = 'SPORTS_TEAM'
		self.result[itype] = {}

		# name and description
		self.__setName(itype)
		self.__setDes(itype)

		# sport, arena, founded
		self.result[itype]['Sport'] = ', '.join(getContent(self.res, '/sports/sports_team/sport'))
		self.result[itype]['Arena'] = ', '.join(getContent(self.res, '/sports/sports_team/arena_stadium'))
		self.result[itype]['Founded'] = ' '.join(getContent(self.res, '/sports/sports_team/founded'))

		# championships and locations
		self.result[itype]['Championships'] = getContent(self.res, '/sports/sports_team/championships')
		self.result[itype]['Locations'] = getContent(self.res, '/sports/sports_team/location')

		# leagues
		tmp = []
		for ll in getContent(self.res, '/sports/sports_team/league', ['/sports/sports_league_participation/league']):
			tmp.append(ll[0][0])
		self.result[itype]['Leagues'] = tmp
	
		# coaches and players roster
		self.result[itype]['Coaches'] = getContent(self.res, '/sports/sports_team/coaches', \
			['/sports/sports_team_coach_tenure/coach', '/sports/sports_team_coach_tenure/position', \
			'/sports/sports_team_coach_tenure/from', '/sports/sports_team_coach_tenure/to'])
		self.result[itype]['PlayersRoster'] = getContent(response, '/sports/sports_team/roster', \
			['/sports/sports_team_roster/player', '/sports/sports_team_roster/number', '/sports/sports_team_roster/position', \
			'/sports/sports_team_roster/from', '/sports/sports_team_roster/to'])

	# define order
	def __typeOrder(self, t):
		return self.typeOrder[t]
	
	def __personOrder(self, x):
		return self.attrOrder['PERSON'][x]

	def __authorOrder(self, x):
		return self.attrOrder['AUTHOR'][x]

	def __actorOrder(self, x):
		return self.attrOrder['ACTOR'][x]

	def __bpOrder(self, x):
		return self.attrOrder['BUSINESS_PERSON'][x]

	def __leagueOrder(self, x):
		return self.attrOrder['LEAGUE'][x]

	def __stOrder(self, x):
		return self.attrOrder['SPORTS_TEAM'][x]

	# format line: sing line or multiple line
	def __formatLine(self, line, linewidth, single = True):
		if single:
			if len(line) > linewidth:
				line = line[:linewidth - 4] + '... '

			else:
				line = line + ' ' * (linewidth - len(line))

			return line

		res = []
		words = line.split()
		ll = ''
		for word in words:
			if len(ll + ' ' + word) > linewidth:
				ll = ll + ' ' * (linewidth - len(ll))
				res.append(ll)
				ll = word

			else:
				ll = word if not ll else ll + ' ' + word

		if ll:
			ll = ll + ' ' * (linewidth - len(ll))
			res.append(ll)

		return res

	# format title for each attribute
	def __formatTitle(self, title, indent):
		title = ' ' + title + ': '
		title = title + ' ' * (indent - len(title))
		return title
		
	# format content for different types
	def __formatContent(self, k, length):
		res = []
		if k == 'Name':
			res = self.__formatLine(result[k], length)

		elif k == 'Description':
			tmp = ' '.join(result[k].split('\n'))
			res = self.__formatLine(tmp, length, False)

		elif k in ['Birthday', 'Place of birth', 'Death', 'Slogan', 'Sport', 'Championship', 'Arena', 'Official Website', 'Founded']:
			res = self.__formatLine(result[k], length)

		elif k in ['Siblings', 'Spouses', 'Books', 'Books about', 'Influenced', 'Influenced By', \
			'Founded', 'Teams', 'Championships', 'Leagues', 'Locations']:
			for tmp in result[k]:
				res.append(self__formatLine(tmp, length))
			

	def output(self, width = 100):
		# sort types
		sorted_types = sorted(self.result.keys(), key=self.__typeOrder)
		
		# set the indent and the width of line of the content
		attrs = []
		for t in sorted_types:
			for k in self.result[t].keys():
				if self.result[t][k]:
					attrs.append(k)

		indent = max(len(item) for item in attrs) + 3		# 3 for : and two spaces
		linewidth = width - indent - 2						# 2 for the leftmost and rightmost |
		breakline = ' ' + '-' * (width - 2) + ' '
		
		# print header
		printtype = []
		printtype.extend(sorted_types)
		if 'PERSON' in printtype:
			printtype.remove('PERSON')

		content = self.name + '(' + ', '.join(printtype) + ')' if printtype else self.name
		content = ' ' * (width / 2 - len(content) / 2) + content
		header = '|' + content + ' ' * (width - 2 - len(content)) + '|'
		print breakline + '\n' + header + '\n' + breakline

		# print contents
		# sort attributes for each type
		for t in sorted_types:
			if t == 'PERSON':
				for k in sorted(self.result[t].keys(), key=self.__personOrder):
					if not self.result[t][k]:
						continue
						
					title = self.__formatTitle(k, indent)
					if k in ['Name', 'Birthday', 'Place of birth', 'Death']:
						print '|' + title + self.__formatLine(self.result[t][k], linewidth) + '|'

					if k in ['Siblings', 'Spouses']:
						for i, item in enumerate(self.result[t][k]):
							if i == 0:
								print '|' + title + self.__formatLine(item, linewidth) + '|'
							
							else:
								print '|' + ' ' * indent + self.__formatLine(item, linewidth) + '|'

					if k == 'Description':
						tmp = ' '.join(self.result[t][k].split('\n'))
						des = self.__formatLine(tmp, linewidth, False)
						for i, item in enumerate(des):
							if i == 0:
								print '|' + title + item + '|'
							
							else:
								print '|' + ' ' * indent + item + '|'

					print breakline

			if t == 'AUTHOR':
				for k in sorted(self.result[t].keys(), key=self.__authorOrder):
					if not self.result[t][k]:
						continue

					title = self.__formatTitle(k, indent)
					for i, item in enumerate(self.result[t][k]):
						if i == 0:
							print '|' + title + self.__formatLine(item, linewidth) + '|'
						
						else:
							print '|' + ' ' * indent + self.__formatLine(item, linewidth) + '|'
				
					print breakline

			if t == 'ACTOR':
				for k in sorted(self.result[t].keys(), key=self.__actorOrder):
					if not self.result[t][k]:
						continue

					title = self.__formatTitle(k, indent)
					if k == 'Films':
						# print sub header
						c1title = self.__formatLine('| Film Name', linewidth / 2)
						c2title = self.__formatLine('| Character', linewidth - len(c1title))
						print '|' + title + c1title + c2title + '|'
						print '|' + ' ' * indent + '-' * linewidth

						# print sub content
						for item in self.result[t][k]:
							tmp = []
							for tt in item:
								tt = '' if not tt else tt[0]
								tmp.append(tt)

							c1 = self.__formatLine('| ' + tmp[0], linewidth / 2) 
							c2 = self.__formatLine('| ' + tmp[1], linewidth - len(c1))
							print '|' + ' ' * indent + c1 + c2 + '|'

					print breakline

			if t == 'BUSINESS_PERSON':
				for k in sorted(self.result[t].keys(), key=self.__bpOrder):
					if not self.result[t][k]:
						continue
				
					title = self.__formatTitle(k, indent)
					if k == 'Founded':
						for i, item in enumerate(self.result[t][k]):
							if i == 0:
								print '|' + title + self.__formatLine(item, linewidth) + '|'
							
							else:
								print '|' + ' ' * indent + self.__formatLine(item, linewidth) + '|'

					if k in ['Leadership', 'Board Member']:
						# set the width of each columns
						len2 = linewidth * 2 / 9
						len1 = linewidth - len2 * 3
						
						# print sub header
						c1t = self.__formatLine('| Organization', len1)
						c2t = self.__formatLine('| Role', len2)
						c3t = self.__formatLine('| Title', len2)
						c4t = self.__formatLine('| From / To', len2)
						print '|' + title + c1t + c2t + c3t + c4t + '|'
						print '|' + ' ' * indent + '-' * linewidth

						# print sub content
						for item in self.result[t][k]:
							tmp = []
							for tt in item:
								tt = '' if not tt else tt[0]
								tmp.append(tt)

							c1 = self.__formatLine('| ' + tmp[0], len1) 
							c2 = self.__formatLine('| ' + tmp[1], len2)
							c3 = self.__formatLine('| ' + tmp[2], len2)
							# generate: (from / to)
							period = ''
							if tmp[3] or tmp[4]:
								tmp[4] = 'now' if not tmp[4] else tmp[4]
								period = '(' + tmp[3] + ' / ' + tmp[4] + ')'

							c4 = self.__formatLine('| ' + period, len2)
							print '|' + ' ' * indent + c1 + c2 + c3 + c4 + '|'

					print breakline

			if t == 'LEAGUE':
				for k in sorted(self.result[t].keys(), key=self.__leagueOrder):
					if not self.result[t][k]:
						continue
				
					title = self.__formatTitle(k, indent)
					if k in ['Name', 'Slogan', 'Sport', 'Championship', 'Official Website']:
						print '|' + title + self.__formatLine(self.result[t][k], linewidth) + '|'

					if k == 'Description':
						tmp = ' '.join(self.result[t][k].split('\n'))
						des = self.__formatLine(tmp, linewidth, False)
						for i, item in enumerate(des):
							if i == 0:
								print '|' + title + item + '|'
							
							else:
								print '|' + ' ' * indent + item + '|'

					if k == 'Teams':
						for i, item in enumerate(self.result[t][k]):
							if i == 0:
								print '|' + title + self.__formatLine(item, linewidth) + '|'
							
							else:
								print '|' + ' ' * indent + self.__formatLine(item, linewidth) + '|'

					print breakline

			if t == 'SPORTS_TEAM':
				for k in sorted(self.result[t].keys(), key=self.__stOrder):
					if not self.result[t][k]:
						continue

					title = self.__formatTitle(k, indent)
					if k in ['Name', 'Sport', 'Arena', 'Founded']:
						print '|' + title + self.__formatLine(self.result[t][k], linewidth) + '|'

					if k == 'Description':
						tmp = ' '.join(self.result[t][k].split('\n'))
						des = self.__formatLine(tmp, linewidth, False)
						for i, item in enumerate(des):
							if i == 0:
								print '|' + title + item + '|'
							
							else:
								print '|' + ' ' * indent + item + '|'

					if k in ['Championships', 'Leagues', 'Locations']:
						for i, item in enumerate(self.result[t][k]):
							if i == 0:
								print '|' + title + self.__formatLine(item, linewidth) + '|'
							
							else:
								print '|' + ' ' * indent + self.__formatLine(item, linewidth) + '|'

					if k == 'Coaches':
						# set the width of each columns
						clen = linewidth / 3
						cclen = linewidth - 2 * clen
						
						# print sub header
						c1t = self.__formatLine('| Name', clen)
						c2t = self.__formatLine('| Position', clen)
						c3t = self.__formatLine('| From / To', cclen)
						print '|' + title + c1t + c2t + c3t + '|'
						print '|' + ' ' * indent + '-' * linewidth

						# print sub content
						for item in self.result[t][k]:
							tmp = []
							for tt in item:
								tt = '' if not tt else tt[0]
								tmp.append(tt)

							c1 = self.__formatLine('| ' + tmp[0], clen) 
							c2 = self.__formatLine('| ' + tmp[1], clen)
							# generate: (from / to)
							period = ''
							if tmp[2] or tmp[3]:
								tmp[3] = 'now' if not tmp[3] else tmp[3]
								period = '(' + tmp[2] + ' / ' + tmp[3] + ')'

							c3 = self.__formatLine('| ' + period, cclen)
							print '|' + ' ' * indent + c1 + c2 + c3 + '|'

					if k == 'PlayersRoster':
						# set the width of each columns
						clen = linewidth / 4
						cclen = linewidth - clen * 3

						# print sub header
						c1t = self.__formatLine('| Name', clen)
						c2t = self.__formatLine('| Number', clen)
						c3t = self.__formatLine('| Position', clen)
						c4t = self.__formatLine('| From / To', cclen)
						print '|' + title + c1t + c2t + c3t + c4t + '|'
						print '|' + ' ' * indent + '-' * linewidth

						# print sub content
						for item in self.result[t][k]:
							tmp = []
							for tt in item:
								tt = '' if not tt else tt[0]
								tmp.append(tt)

							c1 = self.__formatLine('| ' + tmp[0], clen) 
							c2 = self.__formatLine('| ' + tmp[1], clen)
							c3 = self.__formatLine('| ' + tmp[2], clen)
							# generate: (from / to)
							period = ''
							if tmp[3] or tmp[4]:
								tmp[4] = 'now' if not tmp[4] else tmp[4]
								period = '(' + tmp[3] + ' / ' + tmp[4] + ')'

							c4 = self.__formatLine('| ' + period, cclen)
							print '|' + ' ' * indent + c1 + c2 + c3 + c4 + '|'

					print breakline

def search(query, api_key):
	service_url = 'https://www.googleapis.com/freebase/v1/search'
	params = {
		'query': query,
		'key': api_key
	}
	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())
	return [result['mid'] for result in response['result']]

def topic(topic_id, api_key):
	service_url = 'https://www.googleapis.com/freebase/v1/topic'
	params = {
		'key': api_key
	}
	url = service_url + topic_id + '?' + urllib.urlencode(params)
	return json.loads(urllib.urlopen(url).read())['property']

def filtertype(response):
	res = []
	for value in response['/type/object/type']['values']:
		if (value['id'] in FREEBASEMAP.keys()) and (value['id'] not in res):
			res.append(value['id'])
	return res

def run(query, api_key = 'AIzaSyD-DxMBEDLEzKmCW5yWoyJ8gbMUO0_bXuY'):
	query = 'aldrin'
	mids = search(query.strip(), api_key)
	if not mids:
		print 'No related information about query [' + query + '] was found!'
		sys.exit(0)
	response = []
	types = []
	for i, mid in enumerate(mids):
		response = topic(mid, api_key)
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

run()
