
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
	keywords = Column("keywords", TEXT)
	citings = Column("citings", TINYTEXT)
	citeds = Column("citeds", TINYTEXT)
	conference = Column("conference", TINYTEXT)
	published = Column("published", DATETIME)
	url = Column("url", TINYTEXT)
	timestamp = Column("timestamp", DATETIME)
	path = Column("path", TINYTEXT)
	

	def __init__(self, id="", title="", authors="", keywords="", citings="", citeds="", conference = "", published = "", url = "", timestamp="", path=""):
		import mysql_operator
		self.db = mysql_operator.Mysql_operator()

		self.id = id
		self.title = title
		self.authors = authors
		self.keywords = keywords
		self.citings = citings
		self.citeds = citeds
		self.conference = conference
		if published == "":
			self.published = None
		else:
			self.published = published
		self.url = url
		if timestamp == "":
			self.timestamp = None
		else:
			self.timestamp = timestamp
		self.path = path

	def __repr__(self):
		return 'Table_papers'
	
	
	def insert(self):
		import mysql_operator
		db = mysql_operator.Mysql_operator()
		if self.id == "":
			self.id = db.get_available_id(__class__)
		db.insert(self)
		db.session.expunge(self)
		db.session.close()
	
	def is_visited(self):
		import mysql_operator
		db = mysql_operator.Mysql_operator()
	
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
			"title: " + self.title + ", " + 
			"authors: " + self.authors + ", " + 
			"keywords: " + self.keywords + ", " + 
			"citings: " + self.citings + ", " + 
			"citeds: " + self.citeds + ", " + 
			"conference: " + self.conference + ", " + 
			"published: " + str(self.published) + ", " + 
			"url: " + self.url + ", " + 
			"timestamp: " + str(self.timestamp) + ", " +
			"path: " + self.path + ", " + 
		"}")
