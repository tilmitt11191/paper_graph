
# -*- coding: utf-8 -*-

import unittest
import sys,os

class MySQL_test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
		from log import Log as l
		cls.log = l().getLogger()

		cls.log.info("\n\nMySQL_test.setUpClass finished.\n---------- start ---------")
	
	def setUp(self):
		import sqlalchemy
		self.engine = sqlalchemy.create_engine("mysql+pymysql://alladmin:admin@localhost/paper_graph?charset=utf8", echo=False)
		from sqlalchemy.orm import sessionmaker
		Session = sessionmaker(bind=self.engine)
		self.session = Session()

	
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
		
	
	def test_insert_a_title(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		title = "Behind the Game: Exploring the Twitch Streaming Platform"

		import time
		timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
		import table_papers
		initial_num = self.session.query(table_papers.Table_papers).count()
		self.assertEqual(initial_num, self.session.query(table_papers.Table_papers).count())
		
		paper = table_papers.Table_papers(
			id=1,
			title=title,
			timestamp=timestamp
		)
		#print(paper.get_vars())
		self.assertEqual(initial_num, self.session.query(table_papers.Table_papers).count())
		self.session.add(paper)
		self.assertEqual(initial_num + 1, self.session.query(table_papers.Table_papers).count())
		self.session.commit()
		
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

if __name__ == '__main__':
	unittest.main()


