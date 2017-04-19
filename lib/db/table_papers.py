
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
	authors = Column("authors", TEXT)
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
		if self.id == "":
			self.id = self.get_id()
		self.title = self.title.encode('utf-8')
		self.authors = self.authors.encode('utf-8')
		self.keywords = self.keywords.encode('utf-8')
		self.db.insert(self)
		self.title = self.title.decode('utf-8')
		self.authors = self.authors.decode('utf-8')
		self.keywords = self.keywords.decode('utf-8')
		self.db.session.expunge(self)
		self.db.close()
	
	def is_visited(self):
		import mysql_operator
		db = mysql_operator.Mysql_operator()
	
	def renewal_insert(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

		#check duplication and insert
		records = self.db.session.query(__class__).filter(__class__.title==self.title.encode('utf-8')).all()
		if len(records) == 0: #new record
			self.insert()
			return 0
		
		merge_id_list = []
		for record in records:
			merge_id_list.append(record.id)
			
		vars = ["authors", "keywords", "citings", "citeds", "conference", "published", "url", "path"]
		for var in vars:
			for record in records:
				self.log.debug("record.id[" + str(record.id) + "]")
				self.log.debug("var[" + var + "], self[" + str(eval("self." + var)) + "], record[" + str(eval("record." + var)) + "]")
				tmp_timestamp = self.timestamp

				if eval("record." + var) == None or eval("record." + var) == "":
					self.log.debug("records." + var + " == None")
				elif eval("self." + var) == None or eval("self." + var) == "":
					self.log.debug("self." + var + " == None")
					#tmp = eval("self." + var)
					#tmp = eval("record." + var)
					exec("self." + var + " = record." + var)
					self.log.debug("->var[" + var + "], self[" + str(eval("self." + var)) + "], record[" + str(eval("record." + var)) + "]")
					tmp_timestamp = record.timestamp
				else:
					self.log.debug(var + " is not none. compare timestamps")
					## todo: check type(timestamp)
					if tmp_timestamp == None or record.timestamp == None or self.compare_timestamps(old=tmp_timestamp, new=record.timestamp):
						##if record.timestamp is newer
						exec("self." + var + " = record." + var)
						self.log.debug("->var[" + var + "], self[" + str(eval("self." + var)) + "], record[" + str(eval("record." + var)) + "]")
						tmp_timestamp = record.timestamp
					#except:
						#m = "caught exception at tmp_timestamp[" + str(tmp_timestamp) + "] < record.timestamp[" + str(record.timestamp) + "]"
						#self.log.warning(m)
						#print(m)
		
		for record in records:
			self.db.delete(record)
		self.id = self.get_id()
		import time
		self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
		self.insert()
		
		##merge citations
		self.log.debug("merge[" + str(merge_id_list) + "] to self.id[" + str(self.id) + "]")
		for merge_id in merge_id_list:
			from table_citations import Table_citations
			from sqlalchemy import and_, or_
			merge_records = self.db.session.query(Table_citations).filter(or_(Table_citations.start==merge_id, Table_citations.end==merge_id)).all()
			self.log.debug("id[" + str(merge_id) + "].records[" + str(len(merge_records)) + "]")
			for merge_record in merge_records:
				self.merge_citations(merge_record, merge_id_list, survival_id=self.id, delete_id=merge_id)
				
		self.db.close()
		
	def merge_citations(self, merge_record, merge_id_list, survival_id, delete_id):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.debug("from[" + str(merge_record.start) + "]to[" + str(merge_record.end) + "]")
		self.log.debug("survival_id[" + str(survival_id) + "], delete_id[" + str(delete_id) + "]")
		from table_citations import Table_citations
		

		##is delete_id start or end?
		if merge_record.start in merge_id_list and merge_record.end in merge_id_list:
			self.log.debug("start[" + str(merge_record.start) + "] and end[" + str(merge_record.end) + "] are merge_id. delete.")
			self.log.debug("delete(merge_record)")
			self.db.delete(merge_record)
			
		#elif merge_record.start == delete_id and not merge_record.end in merge_id_list:
		elif merge_record.start == delete_id:
			self.log.debug("start[" + str(delete_id) + "] is delete_id. end[" + str(merge_record.end) + "]")
			self.log.debug("delete(merge_record)")
			self.db.delete(merge_record)
			citation = Table_citations(start=survival_id, end=merge_record.end)
			citation.renewal_insert()
			citation.close()
		#elif merge_record.end == delete_id and not merge_record.end in merge_id_list:
		elif merge_record.end == delete_id:
			self.log.debug("end[" + str(merge_record.end) + "] is delete_id. start[" + str(merge_record.start) + "]")
			citation = Table_citations(start=merge_record.start, end=survival_id)
			self.log.debug("delete(merge_record)")
			self.db.delete(merge_record)
			citation.renewal_insert()
			citation.close()
			
	def compare_timestamps(self, old, new):
		self.log.debug("compare old_timestamp[" + str(old) + "] < new[" + str(new) + "]?")
		old_str = str(old)
		new_str = str(new)
		if old_str < new_str:
			self.log.debug("return true")
			return True
		else:
			self.log.debug("return false")
			return False
	
	
	def get_id(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")		
		
		##when the records which have same title exist,
		##the id is smallest one of records.
		records = self.db.session.query(__class__).filter(__class__.title==self.title.encode('utf-8')).all()
		if len(records) == 0: #new record
			return self._get_available_id()
			
		id = records[0].id
		for record in records:
			if id > record.id:
				id = record.id
		return id
	
	def _get_available_id(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
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
