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

# format line: sing line or multiple line
def formatLine(line, linewidth, single = True):
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
def formatTitle(title, indent):
	title = ' ' + title + ': '
	title = title + ' ' * (indent - len(title))
	return title
