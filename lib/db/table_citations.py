
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
		self.close()

	def renewal_insert(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.debug(str(self.start) + " to " + str(self.end))
		#check duplication and insert
		from sqlalchemy import and_
		records = self.db.session.query(__class__).filter(and_(__class__.start==self.start, __class__.end==self.end)).all()
		self.log.debug("records = self.db.session.query(__class__).filter(__class__.start==" + str(self.start) + " and __class__.end==" + str(self.end) + ").all()")
		self.log.debug("len(records)[" + str(len(records)) + "]")
		if len(records) == 0: #new record
			self.log.debug("new citation")
			self.id = self.db.get_available_id(__class__)
			self.insert()
		elif len(records) == 1:
			self.log.debug("already registed")
			self.close()
		else:
			self.log.debug("duplicated")
			self.close()
	
	def close(self):
		self.db.session.close()
		self.db.close()
	
	def get_vars(self):
		return("{"+
			"id: " + str(self.id) + ", " + 
			"start: " + str(self.start) + ", " + 
			"end: " + str(self.end) + 
		"}")


