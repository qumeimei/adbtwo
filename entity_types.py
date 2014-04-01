from util import *

# global variables
FREEBASEMAP = {
	'/people/person': 'Person',
	'/book/author': 'Author',
	'/film/actor': 'Actor',
	'/tv/tv_actor': 'Actor',
	'/organization/organization_founder': 'BusinessPerson',
	'/business/board_member': 'BusinessPerson',
	'/sports/sports_league': 'League',
	'/sports/sports_team': 'SportsTeam',
	'/sports/professional_sports_team': 'SportsTeam'
}

class Person:
	def __init__(self, response):
		self.name = getContent(response, '/type/object/name')
		self.birthday = getContent(response, '/people/person/date_of_birth')
		self.placeOfBirth = getContent(response, '/people/person/place_of_birth')
		self.deathPlace = getContent(response, '/people/deceased_person/place_of_death')
		self.deathDate = getContent(response, '/people/deceased_person/date_of_death')
		self.deathCause = getContent(response, '/people/deceased_person/cause_of_death')
		self.siblings = getContent(response, '/people/person/sibling_s', ['/people/sibling_relationship/sibling'])
		# define the keys that the spouses field should contain
		spouse_keys = ['/people/marriage/spouse', '/people/marriage/from', '/people/marriage/to', '/people/marriage/location_of_ceremony']
		self.spouses = getContent(response, '/people/person/spouse_s', spouse_keys)
		# get the first description if there exists multiple ones
		self.description = getContent(response, '/common/topic/description', None, 'value')
		self.description = self.description[0] if self.description else []
	
	def toString(self):
		return 'PERSON'
	
	def output(self):
		print self.toString()
		attrs = vars(self)
		print '\n'.join('%s : %s' % item for item in attrs.items())
	
class Author:
	def __init__(self, response):
		self.books = getContent(response, '/book/author/works_written')
		self.booksAbout = getContent(response, '/book/book_subject/works')
		self.influenced = getContent(response, '/influence/influence_node/influenced')
		self.influencedBy = getContent(response, '/influence/influence_node/influenced_by')

	def toString(self):
		return 'AUTHOR'
		
	def output(self):
		print self.toString()
		attrs = vars(self)
		print '\n'.join('%s : %s' % item for item in attrs.items())
	
class Actor:
	def __init__(self, response):
		# list of entities
		# entity: [[film name], [character]]
		film_keys = ['/film/performance/film', '/film/performance/character']
		self.films = getContent(response, '/film/actor/film', film_keys)
	def toString(self):
		return 'ACTOR'

	def output(self):
		print self.toString()
		attrs = vars(self)
		print '\n'.join('%s : %s' % item for item in attrs.items())
	
class BusinessPerson:
	def __init__(self, response):
		# leadership and boardMember are lists of entities
		# an entity of the form: from to organization role title
		leader_keys = ['/organization/leadership/organization', '/organization/leadership/role', '/organization/leadership/title', '/organization/leadership/from', '/organization/leadership/to']
		self.leadership = getContent(response, '/business/board_member/leader_of', leader_keys)
		bordmem_keys = ['/organization/organization_board_membership/organization', '/organization/organization_board_membership/role', '/organization/organization_board_membership/title', '/organization/organization_board_membership/from', '/organization/organization_board_membership/to']
		self.boardMember = getContent(response, '/business/board_member/organization_board_memberships', keys)
		self.founded = getContent(response, '/organization/organization_founder/organizations_founded')

	def toString(self):
		return 'BUSINESS_PERSON'

	def output(self):
		print self.toString()
		attrs = vars(self)
		print '\n'.join('%s : %s' % item for item in attrs.items())
	
class League:
	def __init__(self, response):
		self.name = getContent(response, '/type/object/name')
		self.championship = getContent(response, '/sports/sports_league/championship')
		self.sport = getContent(response, '/sports/sports_league/sport')
		self.slogan = getContent(response, '/organization/organization/slogan')
		self.website = getContent(response, '/common/topic/official_website')
		self.teams = getContent(response, '/sports/sports_league/teams', ['/sports/sports_league_participation/team'])
		# get the first description if there exists multiple ones
		self.description = getContent(response, '/common/topic/description', None, 'value')
		self.description = self.description[0] if self.description else []

	def toString(self):
		return 'LEAGUE'

	def output(self):
		print self.toString()
		attrs = vars(self)
		print '\n'.join('%s : %s' % item for item in attrs.items())

class SportsTeam:
	def __init__(self, response):
		self.name = getContent(response, '/type/object/name')
		self.sport = getContent(response, '/sports/sports_team/sport')
		self.arena = getContent(response, '/sports/sports_team/arena_stadium')
		self.championships = getContent(response, '/sports/sports_team/championships')
		# name position from to
		coach_keys = ['/sports/sports_team_coach_tenure/coach', '/sports/sports_team_coach_tenure/position', '/sports/sports_team_coach_tenure/from', '/sports/sports_team_coach_tenure/to']
		self.coaches = getContent(response, '/sports/sports_team/coaches', coach_keys)
		self.founded = getContent(response, '/sports/sports_team/founded')
		self.leagues = getContent(response, '/sports/sports_team/league', ['/sports/sports_league_participation/league'])
		self.locations = getContent(response, '/sports/sports_team/location')
		# name position number from to
		roster_keys = ['/sports/sports_team_roster/player', '/sports/sports_team_roster/number', '/sports/sports_team_roster/position', '/sports/sports_team_roster/from', '/sports/sports_team_roster/to']
		self.roster = getContent(response, '/sports/sports_team/roster', roster_keys)
		# get the first description if there exists multiple ones
		self.description = getContent(response, '/common/topic/description', None, 'value')
		self.description = self.description[0] if self.description else []

	def toString(self):
		return 'SPORTS_TEAM'

	def output(self):
		print self.toString()
		attrs = vars(self)
		print '\n'.join('%s : %s' % item for item in attrs.items())

class QueryItem:
	def __init__(self, types, response):
		self.data = []
		flag1 = True
		flag2 = True
		flag3 = True
		for atype in types:
			if FREEBASEMAP[atype] == 'Person':
				self.data.append(Person(response))
				continue
			if FREEBASEMAP[atype] == 'Author':
				self.data.append(Author(response))
				continue
			if FREEBASEMAP[atype] == 'Actor' and flag1:
				flag1 = False
				self.data.append(Actor(response))
				continue
			if FREEBASEMAP[atype] == 'BusinessPerson' and flag2:
				flag2 = False
				self.data.append(BusinessPerson(response))
				continue
			if FREEBASEMAP[atype] == 'League':
				self.data.append(League(response))
				continue
			if FREEBASEMAP[atype] == 'SportsTeam' and flag3:
				flag3 = False
				self.data.append(SportsTeam(response))

	def output(self):
		for data in self.data:
			data.output()
