class Question:
	def __init__(self, api_key):
		self.api_key = api_key
	
	def run(self, query, single = True):
		query = query.strip()
		if single:
			print 'Let me see...'
		else:
			print 'Query-Question: ' + query
		
		# answer question
