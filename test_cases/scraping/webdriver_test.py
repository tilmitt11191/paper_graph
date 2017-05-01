
# -*- coding: utf-8 -*-

import unittest
import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/scraping")
from phantomjs_ import PhantomJS_


class webdriver_test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
		from conf import Conf
		cls.conf = conf = Conf()
		from log import Log as l
		cls.log = l().getLogger()
		cls.driver = PhantomJS_()
		


		cls.log.info("\n\n"+__class__.__name__+ "."+sys._getframe().f_code.co_name+" finished.\n---------- start ---------")
	
	def setUp(self):
		pass
		
	"""
	def test_get(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/Xplore/home.jsp"
		self.driver.get(url)
		self.driver.save_current_page("./samples/test_get.png")
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	
	def test_reconnect(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/Xplore/home.jsp"
		self.driver.reconnect(url)
		#self.driver.save_current_page("./samples/test_reconnect.png")
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	
	
	
if __name__ == '__main__':
	unittest.main()

