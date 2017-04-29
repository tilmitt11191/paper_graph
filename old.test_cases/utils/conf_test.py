
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

	def test_var(self):
		from conf import Conf
		print("IEEE_website["+Conf.getconf("IEEE_website")+"]")
		print("IEEE_top_page["+Conf.getconf("IEEE_top_page")+"]")
		paper_url = Conf.getconf("IEEE_website") + "/document/6550394"
		print("paper_url[" + paper_url + "]")

if __name__ == '__main__':
	unittest.main()

