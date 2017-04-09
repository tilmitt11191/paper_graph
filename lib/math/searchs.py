
# -*- coding: utf-8 -*-


#breadth_first_search(root_url_of_paper, get_citings(), 1)

class Searchs():

	@classmethod
	def breadth_first_search(cls, root, order_of_returns, get_nexts_func, *args):
		que = [root]
			
		while que != []:
			returned_values = get_nexts_func(que[0], *args)
			que += returned_values[order_of_returns]
			que.pop(0)
			
		return 0
		

	@classmethod
	def depth_first_search(cls, node, order_of_returns, get_nexts_func, *args):
		returned_values = get_nexts_func(node, *args)
		for next_node in returned_values[order_of_returns]:
			cls.depth_first_search(next_node, order_of_returns, get_nexts_func, *args)
	
		return 0
	
	

