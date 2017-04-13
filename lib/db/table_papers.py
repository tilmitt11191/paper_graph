
# -*- coding: utf-8 -*-

import sys,os

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
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
		from log import Log as l
		self.log = l.getLogger()

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
			self.id = self._get_available_id()
		db.insert(self)
		db.session.expunge(self)
		db.session.close()
	
	def is_visited(self):
		import mysql_operator
		db = mysql_operator.Mysql_operator()
	
	def renewal_insert(self):
		#check duplication and insert
		records = self.db.session.query(__class__).filter(__class__.title==self.title).all()
		if len(records) == 0: #new record
			self._get_available_id()
			self.insert()
			return 0
		
		id_list = []
		for record in records:
			id_list.append(record.id)
			
		vars = ["authors", "keywords", "citings", "citeds", "conference", "published", "url", "path"]
		for var in vars:
			for record in records:
				print("record.id[" + str(record.id) + "]")
				print("var[" + var + "], self[" + str(eval("self." + var)) + "], record[" + str(eval("record." + var)) + "]")
				tmp_timestamp = self.timestamp
				#print("id[" + str(record.id) + "]")
				#print("title[" + record.title + "]")
				#print("authors[" + record.authors + "]")
				#print("keywords[" + record.keywords + "]")
				#print("citings[" + record.citings + "]")
				#print("citeds[" + record.citeds + "]")
				#print("conference[" + record.conference + "]")
				#print("published[" + str(record.published) + "]")
				#print("url[" + record.url + "]")
				#print("timestamp[" + str(record.timestamp) + "]")
				#print("path[" + record.path + "]")

				if eval("record." + var) == None or eval("record." + var) == "":
					print("records." + var + " == None")
				elif eval("self." + var) == None or eval("self." + var) == "":
					print("self." + var + " == None")
					#tmp = eval("self." + var)
					#tmp = eval("record." + var)
					exec("self." + var + " = record." + var)
					print("->var[" + var + "], self[" + str(eval("self." + var)) + "], record[" + str(eval("record." + var)) + "]")
					tmp_timestamp = record.timestamp
				else:
					print(var + " is not none. compare timestamps")
					if tmp_timestamp == None or record.timestamp == None or tmp_timestamp < record.timestamp:
						##if record.timestamp is newer
						#tmp = eval("self." + var)
						#tmp = eval("record." + var)
						exec("self." + var + " = record." + var)
						print("->var[" + var + "], self[" + str(eval("self." + var)) + "], record[" + str(eval("record." + var)) + "]")
						#eval("self." + var) = eval("record." + var)
						tmp_timestamp = record.timestamp
		import time
		self.id = self.get_id()
		self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
		
		##merge citations
		print("merge[" + str(id_list) + "] to self.id[" + str(self.id) + "]")
		for merge_id in id_list:
			from table_citations import Table_citations
			records = self.db.session.query(Table_citations).filter(Table_citations.start==merge_id or Table_citations.end==merge_id).all()
			print("records[" + str(len(records)) + "]")
		
		
 		#self.db.insert(self)
		#self.db.session.expunge(self)
		self.db.session.close()
		
	
	def get_id(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")		
		
		##when the records which have same title exist,
		##the id is smallest one of records.
		records = self.db.session.query(__class__).filter(__class__.title==self.title).all()
		if len(records) == 0: #new record
			return self._get_available_id()
			
		id = records[0].id
		for record in records:
			if id > record.id:
				id = record.id
		return id
	
	def _get_available_id(self):
		previous_id = 0
		for q in self.db.session.query(__class__).order_by(__class__.id):
			if q.id - previous_id >= 2:
				self.log.debug("id[" + str(q.id) + "] - previous_id[" + str(previous_id) + "] > 2. return " + str(previous_id + 1))
				return previous_id + 1
			previous_id = q.id
		self.log.debug("for loop ended. return " + str(previous_id + 1))
		return previous_id + 1

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
