
# -*- coding: utf-8 -*-

class IEEEXplore:
	def __init__(self):
		import sys,os
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
		from log import Log as l
		self.log = l.getLogger()
		self.log.debug("class IEEEXplore created.")
	
	
	