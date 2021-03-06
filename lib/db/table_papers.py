
# -*- coding: utf-8 -*-

import sys,os
import time, datetime
from datetime import timedelta

from sqlalchemy import create_engine, Column
from sqlalchemy.dialects.mysql import INTEGER, TEXT, TINYTEXT, MEDIUMTEXT, DATETIME, DATE
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Table_papers(Base):
	__tablename__ = 'papers'

	id = Column("id", INTEGER, primary_key=True)
	title = Column("title", TEXT)
	authors = Column("authors", TEXT)
	keywords = Column("keywords", TEXT)
	citings = Column("citings", MEDIUMTEXT)
	citeds = Column("citeds", MEDIUMTEXT)
	conference = Column("conference", TINYTEXT)
	published = Column("published", DATE)
	url = Column("url", TINYTEXT)
	abstract_path = Column("abstract_path", TEXT)
	pdf_path = Column("pdf_path", TEXT)
	timestamp = Column("timestamp", DATETIME)
	label =  Column("label", TINYTEXT)
	color =  Column("color", TINYTEXT)


	def __init__(self, id="", title="", authors="", keywords="", citings="", citeds="", conference = "", published = "", url = "", timestamp="", abstract_path="", pdf_path="", label="", color=""):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
		from conf import Conf
		self.conf = Conf()
		from log import Log as l
		self.log = l.getLogger()
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

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
		self.abstract_path = abstract_path
		self.pdf_path = pdf_path
		self.label = label
		self.color = color

	def __repr__(self):
		return 'Table_papers'


	def insert(self):
		if self.id == "":
			self.id = self.get_id()
		vars_to_encode = [
			"title", "authors", "keywords", "abstract_path", "pdf_path"]
		for var in vars_to_encode:
			if eval("self." + var) is not None:
				exec("self." + var + " = self." + var + ".encode('utf-8', 'replace')")
		self.db.insert(self)
		for var in vars_to_encode:
			if eval("self." + var) is not None:
				exec("self." + var + " = self." + var + ".decode('utf-8', 'replace')")

		self.db.session.expunge(self)
		self.close()
		
	def has_already_downloaded(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.debug("paper.title[" + self.title + "]")
		if self.conf.getconf("IEEE_paper_download_period") <= 0:
			self.log.debug("IEEE_paper_download_period <= 0, return False")
			return False
		records = self.db.session.query(__class__).filter(
			__class__.title==self.title.encode('utf-8', 'replace')).all()
		if len(records) == 0:
			self.log.debug("This paper doesnt exist in db. return false")
			return False
		elif len(records) >= 2:
			self.log.warning("need to merge records")
			self.log.warning("title["+self.title+"], len(records)[" + str(len(records)) + "]")

		self.log.debug("This paper exist in db. Number of records is [" + str(len(records)) + "]")
		if records[0].abstract_path == "":
			self.log.debug("but the abstract not downloaded. return False")
			return False
		self.log.debug("and the abstract already downloaded. compare timestamps")

		limit = datetime.datetime.now() - timedelta(days=self.conf.getconf("IEEE_paper_download_period"))
		self.log.debug("limit[" + str(limit) + "], records[" + str(records[0].timestamp) + "]")
		if limit > records[0].timestamp:
			self.log.debug("should renew db. return false")
			return False
		else:
			self.log.debug("recently downloaded. clone paper and return true")
			clone_vars = ["authors",
				"keywords",
				"citings",
				"citeds",
				"conference",
				"published",
				"url",
				"timestamp",
				"abstract_path",
				"pdf_path",
				"label",
				"color"]
			for var in clone_vars:
				exec("self." + var + "= records[0]." + var)
			self.close()
			return True

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

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

		vars = ["authors", "keywords", "citings", "citeds", "conference", "published", "url", "abstract_path", "pdf_path", "label", "color"]
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

		self.close()

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
	def get_citings_array(self):
		return self.citings.split(",")
	def get_citeds_array(self):
		return self.citeds.split(",")

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
	
	def close(self):
		self.db.session.close()
		self.db.close()

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
			"abstract_path: " + self.abstract_path + ", " +
			"pdf_path: " + self.pdf_path + ", " +
			"label: " + self.label + ", " +
			"color: " + self.color + ", " +
		"}")
