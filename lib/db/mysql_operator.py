
# -*- coding: utf-8 -*-

import sys,os

class Mysql_operator:
	def __init__(self):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")

		from log import Log as l
		self.log = l.getLogger()
		self.session = self.establish_session()
		
		self.log.debug("class " + __class__.__name__ + " created.")
	

	def establish_session(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		import sqlalchemy
		from conf import Conf
		engine = sqlalchemy.create_engine(Conf.getconf("myslq_url"), echo=False)
		from sqlalchemy.orm import sessionmaker
		Session = sessionmaker(bind=engine)
		return Session()

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")


	def insert(self, query):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")		
		self.session.add(query)
		self.session.commit()
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	
	def delete(self, query):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		
		# 削除対象のデータを検索
		#found_student = session.query(Student).filter_by(name='桑田 結子').first()

		# 指定したデータを削除
		#session.delete(found_student)
		if(query.__tablename__) == "papers":
			self.session.commit()
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	
	def delete_by_id_from_papers(self, id):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		import table_papers
		paper = table_papers.Table_papers(id=id)
		target = self.session.query(table_papers.Table_papers).filter_by(id=id).first()
		if not target == None:
			self.log.debug("delete id[" + str(id) + "]")
			self.session.delete(target)
			self.session.commit()
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	