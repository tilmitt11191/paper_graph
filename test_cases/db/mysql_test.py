
# -*- coding: utf-8 -*-

import unittest
import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
from table_papers import Table_papers

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
	#http://ieeexplore.ieee.org/document/7402463/
	def setUp(self):
		pass
		#import sqlalchemy
		#self.engine = sqlalchemy.create_engine("mysql+pymysql://alladmin:admin@localhost/paper_graph?charset=utf8", echo=False)
		#from sqlalchemy.orm import sessionmaker
		#Session = sessionmaker(bind=self.engine)
		#self.db.session = Session()
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
	"""
	"""
	def test_insert_a_paper(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		paper = table_papers.Table_papers()
		paper.title = "New directions in cryptography - IEEE Xplore Document"
		paper.authors = "W. Diffie, M. Hellman"
		paper.keywords = "Cryptography"
		paper.citings = ""
		paper.citeds = ""
		paper.conference = "10.1109/TIT.1976.1055638"
		paper.published = "1976-01-01"
		paper.url = "http://ieeexplore.ieee.org/document/1055638/"
		paper.timestamp = "2017-05-02 15:06:18"
		paper.path = "../../data/Newdirectionsincryptography/N     ew directions in cryptography - IEEE Xplore Document.pdf"
		paper.id = paper.get_id()
		
		self.log.debug(paper.get_vars())
		
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""

	"""
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
	"""
	def test_compare_timestamps(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		import time
		from table_papers import Table_papers
		paper = Table_papers(title="Traffic Matrix Prediction and Estimation Based on Deep Learning for Data Center Networks")
		new = time.strftime('%Y-%m-%d %H:%M:%S')
		old = "2017-04-17 11:51:24"
		paper.compare_timestamps(new=new, old=old)
		
		
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_renewal_insert1(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		from table_papers import Table_papers
		paper = Table_papers(title="Usilng Machine Learning Technliques to Identify Botnet Traffic - IEEE Xplore Document")
		print("paper.get_id()[" + str(paper.get_id()) + "] title[" + paper.title + "]")
		paper.renewal_insert()
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

	def test_renewal_insert2(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		from table_papers import Table_papers
		paper = Table_papers(title="Traffic Matrix Prediction and Estimation Based on Deep Learning for Data Center Networks")
		print("paper.get_id()[" + str(paper.get_id()) + "] title[" + paper.title + "]")
		paper.renewal_insert()
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_renewal_insert3(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		import subprocess
		from subprocess import Popen, PIPE
		#p = Popen(["python3", "../../lib/db/delete_all.py"], stdout=PIPE)
		#while 1:
		#	c = p.stdout.read(1)
		#	if not c:
		#		break
		#	print(c)
		#p.wait()
		subprocess.check_output(["python3", "../../test_cases/db/insert_sample_papers.py"])
		subprocess.check_output(["python3", "../../test_cases/db/insert_sample_citations.py"])
		subprocess.check_output(["python3", "../../test_cases/db/insert_sample_edges.py"])
		from table_papers import Table_papers
		paper = Table_papers(title="Traffic Matrix Prediction and Estimation Based on Deep Learning for Data Center Networks")
		self.log.debug("paper.get_id()[" + str(paper.get_id()) + "] title[" + paper.title + "]")
		self.log.debug("paper.renewal_insert()")
		paper.renewal_insert()
		
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_renewal_insert_various(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		paper = Table_papers(title="Field Trial of Long-Reach and High-Splitting λあアｱ-Tunable TWDM-PON,")
		#print("paper.get_id()[" + str(paper.get_id()) + "] title[" + paper.title + "]")
		paper.renewal_insert()
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	def test_paper_has_already_downloaded(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		paper = Table_papers(title="Offloading in Mobile Edge Computing: Task Allocation and Computational Frequency Scaling - IEEE Xplore Document")
		print(str(paper.has_already_downloaded()))
		print(paper.get_vars())
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	def test_inheritanced_papers(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		from table_papers_tests import Table_papers_test1
		paper = Table_papers_test1(title="Traffic Matrix Prediction and Estimation Based on Deep Learning for Data Center Networks")
		paper.insert()
	"""	
	
	
	
	
if __name__ == '__main__':
	unittest.main()


