
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
		from log import Log as l
		self.log = l.getLogger()

		import mysql_operator
		self.db = mysql_operator.Mysql_operator()
		
		self.id = id
		self.start = start
		self.end = end
		self.relevancy = relevancy

	def __repr__(self):
		return 'Table_edges'

	def insert(self):
		if self.id == "":
			self.id = self.db.get_available_id(__class__)
		self.db.insert(self)
		self.db.session.expunge(self)
		self.db.session.close()

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
			"start: " + str(self.start) + ", " + 
			"end: " + str(self.end) + ", " + 
			"relevancy: " + str(self.relevancy) + 
		"}")


