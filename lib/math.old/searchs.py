
# -*- coding: utf-8 -*-


class Searchs():


	def __init__(self, initial_node=0, limit=0):
		self.node = initial_node
		self.limit = limit
		self.times = 0
		self.visited = []


	@classmethod
	def breadth_first_search(cls, root, order_of_returns, get_nexts_func, *args):
		que = [root]
		times = 0
		
		while que != []:
			returned_values = get_nexts_func(que[0], times, *args)
			que += returned_values[order_of_returns]
			que.pop(0)
			
		return 0

	@classmethod
	def depth_first_search(cls, node, times, order_of_returns, get_nexts_func, *args):
		#times += 1
		returned_values = get_nexts_func(node, times, *args)
		for next_node in returned_values[order_of_returns]:
			cls.depth_first_search(next_node, times, order_of_returns, get_nexts_func, *args)
	
		return 0
		
		
	@classmethod
	def breadth_first_search_with_class(cls, search, order_of_returns, get_nexts_func, *args):
		que = [search.node]
		
		while que != []:
			search.node = que[0]
			returned_values = get_nexts_func(search, *args)
			que += returned_values[order_of_returns]
			que.pop(0)
		
		return 0

	@classmethod
	def depth_first_search_with_class(cls, search, order_of_returns, get_nexts_func, *args):
		returned_values = get_nexts_func(search, *args)
		
		for next_node in returned_values[order_of_returns]:
			search.node = next_node
			cls.depth_first_search_with_class(search, order_of_returns, get_nexts_func, *args)
			
		return 0


	

