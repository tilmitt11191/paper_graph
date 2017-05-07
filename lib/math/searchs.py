
# -*- coding: utf-8 -*-
import sys
import time
import inspect
import yaml
import traceback

class Searchs():

	def __init__(self, initial_node=0, limit=-1, que=[], visited=[], times=0):
		self.node = initial_node
		self.limit = limit
		self.que = que
		self.visited = visited
		self.times = times
		if len(self.que) == 0:
			self.que = [self.node]
		elif self.que[0] != self.node:
			self.que.insert(0, self.node)

	@classmethod
	def breadth_first_search(
			cls, search, arrays_to_search, get_nexts_func, *args):
		while search.que != []:
			search.node = search.que[0]
			if search.node not in search.visited:
				try:
					returned_values = get_nexts_func(search, *args)
				except:
					filename = cls.save_current_status(search)
					traceback.print_exc()
					sys.exit("[[EXCEPTION OCCURED]] status saved to" + filename)
				cls.renew_search_que(search, arrays_to_search, returned_values)
			search.visited.append(search.node)
			search.que.pop(0)
		return 0

	@classmethod
	def depth_first_search(
			cls, search, arrays_to_search, get_nexts_func, *args):
		returned_values = get_nexts_func(search, *args)

		for next_node in returned_values[arrays_to_search]:
			search.node = next_node
			cls.depth_first_search_with_class(
				search, arrays_to_search, get_nexts_func, *args)

		return 0

	@classmethod
	def renew_search_que(cls, search, arrays_to_search, returned_values):
		if isinstance(arrays_to_search, int):
			search.que += returned_values[arrays_to_search]
		elif isinstance(arrays_to_search, list):
			for array in arrays_to_search:
				search.que += returned_values[array]
		else:
			print("isinstance type error")
		# delete duplicated elements
		search.que = list(set(search.que))

	# if process stoped due to such as a exception at get_nexts_func,
	# call this method to save, and call restore method to restart process
	@classmethod
	def save_current_status(cls, search):
		status = {}
		filename = "../../var/yaml/save_at_" + \
			str(time.strftime('%Y-%m-%d-%H_%M_%S')) + ".yaml"

		methods = []
		for method in inspect.getmembers(search, inspect.ismethod):
			methods.append(method[0])
		vars = []
		for var in search.__dir__():
			if not var.startswith("_") and not var in methods:
				vars.append(var)

		for var in vars:
			status.update({var: eval("str(search." +var+")")})

		f = open(filename, 'w')
		f.write(yaml.dump(status))
		f.close()

		return filename

	@classmethod
	def restore_status(cls, filename):
		with open(filename, "r") as f:
			status = yaml.load(f)
		search = Searchs()

		methods = []
		for method in inspect.getmembers(search, inspect.ismethod):
			methods.append(method[0])
		for var in search.__dir__():
			if not var.startswith("_") and not var in methods:
				exec("search."+ var + " = status[\"" + var + "\"]")
		return search
