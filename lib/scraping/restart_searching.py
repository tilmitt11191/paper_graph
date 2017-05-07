
# -*- coding: utf-8 -*-

import sys
import os
args = sys.argv
if len(args) < 2:
	print("no saved file path")
saved_file = args[1]
print("saved_file[" + saved_file + "]")

timeout=30

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
from searchs import Searchs

search = Searchs.restore_status(saved_file)
self.log.debug("node: " + search.node)
self.log.debug("limit: " + str(search.limit))
self.log.debug("que: " + str(search.que))
self.log.debug("visited: " + str(search.visited))
self.log.debug("times: " + str(search.times))

Searchs.breadth_first_search(search, [2, 3, 4, 5, 6], xplore.get_attributes_and_download_pdf, driver, path, filename)

driver.close()

print("Finished!!")
