
# -*- coding: utf-8 -*-

import sys,os

from sqlalchemy import create_engine, Column
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Table_citations(Base):
	__tablename__ = 'citations'

	id = Column("id", INTEGER, primary_key=True)
	start = Column("start", INTEGER)
	end = Column("end", INTEGER)

	def __init__(self, id="", start="", end=""):
	
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
		from log import Log as l
		self.log = l.getLogger()
		
		import mysql_operator
		self.db = mysql_operator.Mysql_operator()

		self.id = id
		self.start = start
		self.end = end

	def __repr__(self):
		return 'Table_citations'

	def insert(self):
		if self.id == "":
			self.id = self.db.get_available_id(__class__)
		self.db.insert(self)
		self.db.session.expunge(self)
		self.db.session.close()

	def renewal_insert(self):
		#check duplication and insert
		records = self.db.session.query(__class__).filter(__class__.start==self.start and __class__.end==end).all()
		if len(records) == 0: #new record
			print("new citation")
			self.db.get_available_id(self)
			self.insert()
			return 0
		elif len(records) == 1:
			print("already registed")
			return 0
		else:
			print("duplicated")
		#for record in records:
			
	
	def get_vars(self):
		return("{"+
			"id: " + str(self.id) + ", " + 
			"start: " + str(self.start) + ", " + 
			"end: " + str(self.end) + 
		"}")


