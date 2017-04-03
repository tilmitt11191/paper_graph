
# -*- coding: utf-8 -*-

class IEEEXplore:
	def __init__(self):
		import sys,os
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
		from log import Log as l
		self.log = l.getLogger()
		self.log.debug("class IEEEXplore created.")
	
	def get_papers_of_new_conferences(self, conference_num):
		self.log.info("get_papers_of_new_conferences(conference_num=" + str(conference_num) + ") start.")
	