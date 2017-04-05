
# -*- coding: utf-8 -*-


from sqlalchemy import create_engine, Column
from sqlalchemy.dialects.mysql import INTEGER, TEXT, TINYTEXT, DATETIME
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Table_papers(Base):
	__tablename__ = 'papers'

	id = Column("id", INTEGER, primary_key=True)
	title = Column("title", TEXT)
	authors = Column("authors", TINYTEXT)
	keywords = Column("keywords", TINYTEXT)
	cites = Column("cites", TINYTEXT)
	path = Column("path", TINYTEXT)
	timestamp = Column("timestamp", DATETIME)
	

	def __init__(self, id="", title="", authors="", keywords="", cites="", path="", timestamp=""):
		self.id = id
		self.title = title
		self.authors = authors
		self.keywords = keywords
		self.cites = cites
		self.path = path
		self.timestamp = timestamp

	def __repr__(self):
		return 'Table_papers'

	
	def get_vars(self):
		return("{"+
			"id: " + str(self.id) + ", " + 
			"title: " + self.title + ", " + 
			"authors: " + self.authors + ", " + 
			"keywords: " + self.keywords + ", " + 
			"cites: " + self.cites + ", " + 
			"path: " + self.path + ", " + 
			"timestamp: " + self.timestamp +
		"}")


