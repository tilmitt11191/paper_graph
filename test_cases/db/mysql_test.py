
# -*- coding: utf-8 -*-

import unittest
import sys,os

class MySQL_test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
		from log import Log as l
		cls.log = l().getLogger()
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
		import mysql_operator
		cls.db = mysql_operator.Mysql_operator()

		cls.log.info("\n\nMySQL_test.setUpClass finished.\n---------- start ---------")
	
	def setUp(self):
		#import sqlalchemy
		#self.engine = sqlalchemy.create_engine("mysql+pymysql://alladmin:admin@localhost/paper_graph?charset=utf8", echo=False)
		#from sqlalchemy.orm import sessionmaker
		#Session = sessionmaker(bind=self.engine)
		#self.db.session = Session()
		pass
	"""
	def get_titles_authors_from_deeplearningtraffic(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		sample = "../../test_cases/workspace/samples/deeplearningtraffic.txt"
		if not os.path.exists(sample):
			sys.exit("FILE NOT EXIST")
		titles = []
		authors = []
		f = open(sample, "r")
		line = f.readline()
		while line:
			if "pdf_title" in line:
				titles.append(line.split(":")[1])
			elif "pdf_author" in line:
				authors.append(line.split(":")[1])
			line = f.readline()
		f.close()
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		return titles, authors
		
	"""
	def test_insert_a_title(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		title = "Behind the Game: Exploring the Twitch Streaming Platform"

		import time
		timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
		import table_papers
		initial_num = self.db.session.query(table_papers.Table_papers).count()
		self.assertEqual(initial_num, self.db.session.query(table_papers.Table_papers).count())
		
		paper = table_papers.Table_papers(
			title=title,
			timestamp=timestamp
		)

		self.assertEqual(initial_num, self.db.session.query(table_papers.Table_papers).count())
		paper.insert()
		self.assertEqual(initial_num + 1, self.db.session.query(table_papers.Table_papers).count())
		
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

	"""
	def test_insert_a_title2(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		title = "Behind the Game: Exploring the Twitch Streaming Platform"

		import time
		timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
		import table_papers
		initial_num = self.db.session.query(table_papers.Table_papers).count()

		paper = table_papers.Table_papers(
			id=1,
			title=title,
			timestamp=timestamp
		)
		
		self.db.insert(paper)
		self.assertEqual(initial_num+1, self.db.session.query(table_papers.Table_papers).count())
		
		
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")


	def test_delete_a_title(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		title = "Behind the Game: Exploring the Twitch Streaming Platform"
		
		import table_papers
		paper = table_papers.Table_papers(title=title)
		
		#self.db.delete(paper)
		
		import time
		timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
		paper = table_papers.Table_papers(
			id=1,
			title=title,
			timestamp=timestamp
		)
		
		#self.db.insert(paper)
		paper = table_papers.Table_papers(
			id=1,
			title=title,
			timestamp=timestamp
		)
		self.db.insert(paper)
		self.db.delete_by_id_from_papers(1)
		
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	
	
	def test_init_mysql_operator(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
		import mysql_operator
		self.db = mysql_operator.Mysql_operator()
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	
	def test_get_available_id(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		import table_papers
		id = self.db.get_available_id(table_papers.Table_papers)
		print("available_id[" + str(id) + "]")
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	
	
	
if __name__ == '__main__':
	unittest.main()


