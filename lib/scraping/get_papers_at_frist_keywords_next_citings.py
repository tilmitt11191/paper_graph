
# -*- coding: utf-8 -*-

keywords = "\"edge computing\""
num_of_papers = 1000
path="../../data/" + keywords.replace(" ", "").replace("\"", "") + "/"
filename = "tmp.pdf"
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

if num_of_papers <= 0:
	self.log.warning("initial num_of_papers <= 0")
	sys.exit("initial num_of_papers <= 0")

all_papers, all_citing_urls, all_cited_urls = xplore.get_papers_by_keywords(keywords, num_of_papers, search_options=opts, timeout=timeout)
num_of_papers -= len(all_papers)

if num_of_papers <= 0:
	self.log.info("finished in the way of xplore.get_papers_by_keywords")
	sys.exit()

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
from searchs import Searchs

search = Searchs(que=all_citing_urls, limit=num_of_papers)

Searchs.breadth_first_search_with_class(search, 1, self.xplore.get_attributes_and_download_pdf, driver, path, filename)

driver.close()

print("Finished!!")


