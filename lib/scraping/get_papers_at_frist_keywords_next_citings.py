
# -*- coding: utf-8 -*-

keywords = "\"edge computing\""
num_of_papers = 1000
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

from IEEEXplore import IEEEXplore as X
xplore = X()
from IEEEXplore import Search_options as s
opts = s()
opts.PerPage = 100


if num_of_papers <= 0:
	log.warning("initial num_of_papers <= 0")
	sys.exit("initial num_of_papers <= 0")

all_papers, all_papers_urls, all_citing_urls, all_cited_urls = xplore.get_papers_by_keywords(keywords, num_of_papers, search_options=opts, path=path, filename=filename, timeout=timeout)

if num_of_papers <= 0:
	log.info("finished in the way of xplore.get_papers_by_keywords")
	sys.exit()

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
from searchs import Searchs

driver = xplore.create_driver(timeout=timeout)
search = Searchs(que=all_citing_urls, times=len(all_papers), visited=all_papers_urls, limit=num_of_papers)

Searchs.breadth_first_search_with_class(search, 1, xplore.get_attributes_and_download_pdf, driver, path, filename)

driver.close()

print("Finished!!")


