
# -*- coding: utf-8 -*-


from sqlalchemy import create_engine, Column
from sqlalchemy.dialects.mysql import INTEGER, FLOAT
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Table_edges(Base):
	__tablename__ = 'edges'

	id = Column("id", INTEGER, primary_key=True)
	start = Column("start", INTEGER)
	end = Column("end", INTEGER)
	relevancy = Column("relevancy", FLOAT)
	

	def __init__(self, id="", start="", end="", relevancy=""):
		self.id = id
		self.start = start
		self.end = end
		self.relevancy = relevancy

	def __repr__(self):
		return 'Table_edges'

	
	def get_vars(self):
		return("{"+
			"id: " + str(self.id) + ", " + 
			"start: " + str(self.start) + ", " + 
			"end: " + str(self.end) + ", " + 
			"relevancy: " + str(self.relevancy) + 
		"}")


