
# -*- coding: utf-8 -*-


class Searchs():
	def __init__(self, initial_node=0, limit=-1, que=[], visited=[], times=0):
		self.node = initial_node
		self.limit = limit
		self.que = que
		self.visited = visited
		self.times = times
		if len(self.que) == 0:
			self.que = [self.node]

	@classmethod
	def __breadth_first_search(cls, root, arrays_to_search, get_nexts_func, *args):
		que = [root]
		times = 0

		while que != []:
			returned_values = get_nexts_func(que[0], times, *args)
			que += returned_values[arrays_to_search]
			que.pop(0)

		return 0

	@classmethod
	def __depth_first_search(cls, node, times, arrays_to_search, get_nexts_func, *args):
		#times += 1
		returned_values = get_nexts_func(node, times, *args)
		for next_node in returned_values[arrays_to_search]:
			cls.depth_first_search(next_node, times, arrays_to_search, get_nexts_func, *args)

		return 0


	@classmethod
	def breadth_first_search(cls, search, arrays_to_search, get_nexts_func, *args):
		while search.que != []:
			search.node = search.que[0]
			if search.node not in search.visited:
				returned_values = get_nexts_func(search, *args)
				cls.renew_search_que(search.que, arrays_to_search, returned_values)
			search.visited.append(search.node)
			search.que.pop(0)
		return 0

	@classmethod
	def depth_first_search(cls, search, arrays_to_search, get_nexts_func, *args):
		returned_values = get_nexts_func(search, *args)

		for next_node in returned_values[arrays_to_search]:
			search.node = next_node
			cls.depth_first_search_with_class(search, arrays_to_search, get_nexts_func, *args)

		return 0

	@classmethod
	def renew_search_que(cls, que, arrays_to_search, returned_values):
		if isinstance(arrays_to_search, int):
			que += returned_values[arrays_to_search]
		elif  isinstance(arrays_to_search, list):
			for array in arrays_to_search:
				que +=returned_values[array]
		else:
			print("isinstance type error")
		#delete duplicated elements
		que = list(set(que))
