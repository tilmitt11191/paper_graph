
# -*- coding: utf-8 -*-

import unittest
import sys,os

class IEEEXplore_test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
		from log import Log as l
		cls.log = l().getLogger()

		cls.log.info("\n\nIEEEXplore_test.setUpClass finished.\n---------- start ---------")
	
	def setUp(self):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/scraping")
		from IEEEXplore import IEEEXplore as X
		self.xplore = X()

	"""
	def test_show_options(self):
		self.log.info("test_show_options start")
		self.xplore.show_options()
	"""
	
	"""
	def test_get_papers_by_keywords(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		keywords = "deep learning traffic"
		num_of_papers = 1
		self.xplore.get_papers_by_keywords(keywords, num_of_papers)
	"""

	def test_download_a_paper(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://google.co.jp/"
		#driver = self.xplore.create_driver("http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7874313")
		driver = self.xplore.create_driver(url)
		import urllib
		urllib.urlretrieve(url, 'test.pdf')

		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		
		
			
	"""
	def test_download_papers(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		driver = self.xplore.create_driver("http://ieeexplore.ieee.org/search/searchresult.jsp?queryText=deep%20learning%20traffic")
		self.xplore.download_papers(driver, "../../tmp/output", 1)
		driver.close()
		#http://ieeexplore.ieee.org/document/7874313/
		#http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7874313
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_convert_path_to_url(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = self.xplore.convert_path_to_url("http://ieeexplore.ieee.org/document/7874313/")
		self.assertEqual("http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7874313", url)
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_get_papers_of_new_conferences(self):
		self.log.info("test_get_papers_of_new_conferences start")
		self.xplore.get_papers_of_new_conferences(10)
	"""
if __name__ == '__main__':
	unittest.main()

