#!/usr/bin/python

import sys
import argparse
import time
import os
import socket
import re
import infobox
import question

parser = argparse.ArgumentParser()
parser.add_argument('-key',	metavar = '<Freebase API key>', type = str, nargs = 1)
parser.add_argument('-q', 	metavar = '<query>', 			type = str, nargs = '+')
parser.add_argument('-f', 	metavar = '<file or queries>',	type = str, nargs = 1)
parser.add_argument('-t', 	metavar = '<infobox|question>',	type = str,	nargs = 1)

args = parser.parse_args()

if args.key is None:
	parser.print_usage()
	sys.exit(2)

info = infobox.Infobox(args.key[0])
ques = question.Question(args.key[0])

if args.t is None:
	len1 = 'Welcome to infoxbox creator using Freebase knowledge graph.'
	len2 = 'Created by Jingyi Guo(jg3421) and Yu Zheng(yz2583)'
	len3 = 'Feel curious? Start exploring and have fun... ^_^'
	max_len = max(len(len1), len(len2), len(len3))
	print ' ' + '-' * (max_len + 1)
	print '| ' + len1 + ' ' * (max_len - len(len1)) + '|'
	print '| ' + len2 + ' ' * (max_len - len(len2)) + '|'
	print '| ' + len3 + ' ' * (max_len - len(len3)) + '|'
	print ' ' + '-' * (max_len + 1)
	try:
		while True:
			print ''
			prompt = '[' + time.strftime('%H:%M:%S', time.localtime()) + '] ' + os.getlogin() + '@' + socket.gethostname() + '> '
			query = raw_input(prompt)
			if re.match('^who created .*', query.lower()) is None:
				info.run(query)
			else:
				ques.run(query)

	except KeyboardInterrupt:
		print '\nGoodbye!\n  ^_^'

	except Exception:
		print 'Oooops...something wrong'

	sys.exit(0)

if args.t[0].lower() != 'infobox' and args.t[0].lower() != 'question':
	parser.print_usage()
	sys.exit(2)

if args.t[0].lower() == 'infobox':
	if (args.q is None and args.f is None) or (args.q is not None and args.f is not None):
		parser.print_usage()
		sys.exit(2)
	
	if args.q is not None:
		info.run(' '.join(args.q))
	
	if args.f is not None:
		if not os.path.isfile(args.f[0]):
			print 'Unable to read file:' + args.f[0]
			sys.exit(1)

		f = open(args.f[0], 'r')
		try:
			while True:
				line = f.readline()
				if re.match('\\s+' , line):
					print 'Query-Question:'
					print 'Hmm! Empty query! (-_-)\n'
					continue
				if not line:
					break
				query = line[:-1]
				info.run(query, False)

		except KeyboardInterrupt:
			print '\nGoodbye!\n  ^_^'

		except Exception:
			print 'Oooops...something wrong'

		f.close()
		sys.exit(0)

if args.t[0].lower() == 'question':
	if (args.q is None and args.f is None) or (args.q is not None and args.f is not None):
		parser.print_usage()
		sys.exit(2)
	
	if args.q is not None:
		ques.run(' '.join(args.q))
	
	if args.f is not None:
		if not os.path.isfile(args.f[0]):
			print 'Unable to read file:' + args.f[0]
			sys.exit(1)

		f = open(args.f[0], 'r')
		try:
			while True:
				line = f.readline()
				if re.match('\\s+' , line):
					print 'Query-Question:'
					print 'Hmm! Empty query! (-_-)\n'
					continue
				if not line:
					break
				query = line[:-1]
				ques.run(query, False)

		except KeyboardInterrupt:
			print '\nGoodbye!\n  ^_^'

		except Exception:
			print 'Oooops...something wrong'

		f.close()
		sys.exit(0)
