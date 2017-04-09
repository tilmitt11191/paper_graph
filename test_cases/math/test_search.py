
# -*- coding: utf-8 -*-

import unittest
import sys,os

class Search_test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
		from log import Log as l
		cls.log = l().getLogger()

		cls.log.info("\n\nSearch_test.setUpClass finished.\n---------- start ---------")
	
	def setUp(self):
		pass
	
	###http://kannokanno.hatenablog.com/entry/2013/06/05/175503
	##bfs
	simple_graph = {1: [2, 3, 4],
		2: [5, 6],
		3: [7],
		4: [8, 9],
		5: [],
		6: [10],
		7: [],
		8: [7],
		9: [11],
		10: [],
		11: [],
	}
	def get_nexts_simple(self, node_num, str1, str2):
		print(str(node_num) + ".get_nexts")
		print("str1[" + str1 + "], str2[" + str2 + "]")
		str1 += "str1"
		str2 += "str2"
		return str1, self.simple_graph[node_num]
		
	
	def test_simple_graph(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
		str1 = "str1"
		str2 = "str2"
		from searchs import Searchs
		print("Searchs.breadth_first_search")
		Searchs.breadth_first_search(1, 1, self.get_nexts_simple, str1, str2)
		
		#print("Searchs.depth_first_search")
		#Searchs.depth_first_search(1, 1, self.get_nexts_simple, str1, str2)
		
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")




	
	
if __name__ == '__main__':
	unittest.main()


























