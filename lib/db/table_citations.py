
# -*- coding: utf-8 -*-


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
		self.id = id
		self.start = start
		self.end = end

	def __repr__(self):
		return 'Table_citations'

	def insert(self):
		import mysql_operator
		db = mysql_operator.Mysql_operator()
		if self.id == "":
			self.id = db.get_available_id(__class__)
		db.insert(self)
		db.session.expunge(self)
		db.session.close()

	def renewal_insert(self):
		#check duplication and insert
		import mysql_operator
		db = mysql_operator.Mysql_operator()
		if self.id == "":
			self.id = db.get_available_id(__class__)
		#db.insert(self)
		#db.session.expunge(self)
		db.session.close()
	
	def get_vars(self):
		return("{"+
			"id: " + str(self.id) + ", " + 
			"start: " + str(self.start) + ", " + 
			"end: " + str(self.end) + 
		"}")


