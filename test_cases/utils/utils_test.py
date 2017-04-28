
# -*- coding: utf-8 -*-


import unittest
import sys,os

class Utils_test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
		from log import Log as l
		cls.log = l().getLogger()

		cls.log.info("\n\n"+__class__.__name__+ "."+sys._getframe().f_code.co_name+" finished.\n---------- start ---------")

	def setUp(self):
		pass
	
	def test_log_to_stdout(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.debug("debug comment")
		self.log.info("info comment")
		self.log.warning("warning comment")
		self.log.error("error comment")
		self.log.critical("critical comment")
		

if __name__ == '__main__':
	unittest.main()


