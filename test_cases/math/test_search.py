
# -*- coding: utf-8 -*-

import unittest
import sys,os

check = os.system("pwd")
print(check)
print(sys.version)

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
from searchs import Searchs


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


	def get_nexts_simple(self, search):
		print(str(search.node) + ".get_nexts")
		print("times["+str(search.times)+"], limit["+str(search.limit)+"]")
		print("visited: " + str(search.visited))
		search.times += 1
		if search.times >= search.limit:
			search.que = [search.node]
			return [[]]
		else:
			return [self.simple_graph[search.node]]

	def get_nexts_with_many_arrays(self, search):
		print(str(search.node) + ".get_nexts")
		print("times["+str(search.times)+"], limit["+str(search.limit)+"]")
		print("visited: " + str(search.visited))
		search.times += 1
		if search.times >= search.limit:
			search.que = [search.node]
			return [[],[],[]]
		else:
			print("else")
			return [self.simple_graph[search.node], [1,2,3], [4,5,6]]

	"""
	def test_simple_graph(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

		search = Searchs(initial_node=1, limit=5)

		print("Searchs.breadth_first_search")
		search = Searchs(initial_node=1, limit=5)
		Searchs.breadth_first_search(search, 0, self.get_nexts_simple)
		#print("Searchs.depth_first_search")
		#search = Searchs(initial_node=1, limit=5)
		#Searchs.depth_first_search(search, 0, self.get_nexts_simple)

		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_simple_graph_with_limit_class(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

		search = Searchs(initial_node=1, limit=5)

		print("Searchs.breadth_first_search")
		Searchs.breadth_first_search(search, 0, self.get_nexts_simple)
	"""
	#"""
	def test_simple_graph_with_many_arrays(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

		search = Searchs(initial_node=1, limit=5)

		print("Searchs.breadth_first_search")
		search = Searchs(initial_node=1, limit=5)
		Searchs.breadth_first_search(search, [0,1,2], self.get_nexts_with_many_arrays)
		#print("Searchs.depth_first_search")
		#search = Searchs(initial_node=1, limit=5)
		#Searchs.depth_first_search(search, 0, self.get_nexts_with_many_arrays)

		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	#"""
if __name__ == '__main__':
	unittest.main()
