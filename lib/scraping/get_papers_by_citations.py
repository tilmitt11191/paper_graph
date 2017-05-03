
# -*- coding: utf-8 -*-
#python ../../lib/scraping/get_papers_at_frist_keywords_next_citings.py "\"edge computing\""

import sys
args = sys.argv
if len(args) < 2:
	print("no keywords")
keywords = args[1]
print("keywords[" + keywords + "]")

num_of_papers = 10000
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
log.debug("all_papers[" + str(len(all_papers)) + "]")
log.debug("all_papers_urls[" + str(len(all_papers_urls)) + "]")
log.debug("all_citing_urls[" + str(len(all_citing_urls)) + "]")
log.debug("all_cited_urls[" + str(len(all_cited_urls)) + "]")


if num_of_papers <= len(all_papers):
	log.info("finished in the way of xplore.get_papers_by_keywords")
	sys.exit()

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
from searchs import Searchs

driver = xplore.create_driver(timeout=timeout)
search = Searchs(que=all_citing_urls.extend(all_cited_urls), times=len(all_papers), visited=all_papers_urls, limit=num_of_papers)

Searchs.breadth_first_search(search, [1, 2], xplore.get_attributes_and_download_pdf, driver, path, filename)

driver.close()

print("Finished!!")
