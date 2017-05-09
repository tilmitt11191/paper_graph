
# -*- coding: utf-8 -*-

import sys
import os
args = sys.argv
if len(args) < 2:
	print("no saved file path or pdf save path")
saved_file = args[1]
print("saved_file[" + saved_file + "]")
path = args[2]
if path[-1] != "/":
	path = path + "/"
print("path: " + path)
filename = "title"

timeout=30

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
from searchs import Searchs

from IEEEXplore import IEEEXplore
xplore = IEEEXplore()

search = Searchs.restore_status(saved_file)
print("node: " + search.node)
print("limit: " + str(search.limit))
print("len(que): " + str(len(search.que)))
print("len(visited): " + str(len(search.visited)))
print("times: " + str(search.times))

driver = xplore.create_driver(search.node)

Searchs.breadth_first_search(search, [2, 3, 4, 5, 6], xplore.get_attributes_and_download_pdf, driver, path, filename)

driver.close()

print("Finished!!")
