
# -*- coding: utf-8 -*-

import unittest
class Conf_test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		import sys,os
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
		from log import Log as l
		l = l()
		cls.log = l.getLogger()

		cls.log.info("\n\nConf_test setUpClass finished.\n---------- start ---------")
	
	def test_conf(self):
		from conf import Conf
		print("loglevel["+Conf.getconf("loglevel")+"]")

if __name__ == '__main__':
	unittest.main()

