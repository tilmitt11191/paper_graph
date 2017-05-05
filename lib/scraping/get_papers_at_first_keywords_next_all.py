
# -*- coding: utf-8 -*-

## python ../../lib/db/delete_all.py && :> ../../var/log/log && python ../../lib/scraping/get_papers_at_first_keywords_next_all.py "\"edge computing\"" 10000
## python ../../lib/db/delete_all.py && :> ../../var/log/log && python ../../lib/scraping/get_papers_at_first_keywords_next_all.py "\"New directions in cryptography\"" 100000

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

from IEEEXplore import IEEEXplore as X
xplore = X()
from IEEEXplore import Search_options as s
opts = s()
opts.PerPage = 100


if num_of_papers <= 0:
    log.warning("initial num_of_papers <= 0")
    sys.exit("initial num_of_papers <= 0")

all_papers, all_papers_urls, all_urls_of_papers_with_same_authors, all_urls_of_papers_with_same_keywords, all_citing_urls, all_cited_urls, all_urls_in_conference = xplore.get_papers_by_keywords(keywords, num_of_papers, search_options=opts, path=path, filename=filename, timeout=timeout)
log.debug("all_papers[" + str(len(all_papers)) + "]")
log.debug("all_papers_urls[" + str(len(all_papers_urls)) + "]")
log.debug("all_urls_of_papers_with_same_authors" + str(len(all_urls_of_papers_with_same_authors)) + "]")
log.debug("all_urls_of_papers_with_same_keywords" + str(len(all_urls_of_papers_with_same_keywords)) + "]")
log.debug("all_citing_urls[" + str(len(all_citing_urls)) + "]")
log.debug("all_cited_urls[" + str(len(all_cited_urls)) + "]")
log.debug("all_urls_in_conference" + str(len(all_urls_in_conference)) + "]")

if num_of_papers <= len(all_papers):
    log.info("finished in the way of xplore.get_papers_by_keywords")
    sys.exit()

que = []
que.extend(all_urls_of_papers_with_same_authors)
que.extend(all_urls_of_papers_with_same_keywords)
que.extend(all_citing_urls)
que.extend(all_cited_urls)
que.extend(all_urls_in_conference)


sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
from searchs import Searchs

driver = xplore.create_driver(timeout=timeout)
search = Searchs(que=que, times=len(all_papers), visited=all_papers_urls, limit=num_of_papers)

Searchs.breadth_first_search(search, [2, 3, 4, 5, 6], xplore.get_attributes_and_download_pdf, driver, path, filename)

driver.close()

print("Finished!!")
