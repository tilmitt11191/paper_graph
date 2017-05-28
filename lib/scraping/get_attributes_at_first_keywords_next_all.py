
# -*- coding: utf-8 -*-

#python ../../lib/db/delete_all.py && :> ../../var/log/log && python ../../lib/scraping/get_attributes_at_first_keywords_next_all.py "\"New directions in cryptography\"" 100000


import sys
args = sys.argv
if len(args) < 3:
	print("no keywords or num_of_papers")
keywords = args[1]
print("keywords[" + keywords + "]")

num_of_papers = int(args[2])

path="../../data/" + keywords.replace(" ", "").replace("\"", "") + "/"
filename = "title"
timeout=30

import sys,os
if not os.path.exists(path):
	print("create directory[" + path + "]")
	os.mkdir(path)

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from log import Log as l
log = l.getLogger()
log.info("get_papers_from_IEEE.py start.")
log.info("num_of_papers["+str(num_of_papers)+"]")

from IEEEXplore import IEEEXplore
xplore = IEEEXplore()
from IEEEXplore import Search_options
opts = Search_options()
opts.PerPage = 100

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
from searchs import Searchs


if num_of_papers <= 0:
	log.warning("initial num_of_papers <= 0")
	sys.exit("initial num_of_papers <= 0")

xplore.search_by_keywords(keywords, search_options=opts, timeout=timeout)
urls = xplore.get_urls_of_papers_in_search_results(timeout=timeout)
print("num of urls searched by keywords: " + str(len(urls)))

search = Searchs(initial_node=urls[0], que=urls, times=1, visited=[], limit=num_of_papers)

Searchs.breadth_first_search(search, [2, 3, 4, 5, 6], xplore.get_attributes_of_target_paper_for_bfs, path, filename, timeout)

print("Finished!!")
