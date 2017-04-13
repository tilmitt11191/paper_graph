
# -*- coding: utf-8 -*-

import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from log import Log as l
log = l().getLogger()

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
import mysql_operator
import table_papers
db = mysql_operator.Mysql_operator()

sample = "../../test_cases/workspace/samples/deeplearningtraffic.txt"
if not os.path.exists(sample):
	sys.exit("FILE NOT EXIST")
titles = []
authors = []
f = open(sample, "r")
line = f.readline()
while line:
	if "pdf_title" in line:
		titles.append(line.split(":")[1].strip())
	elif "pdf_author" in line:
		authors.append(line.split(":")[1].strip())
	line = f.readline()
f.close()

#print(str(len(titles))+ ", "+str(titles))
#print(str(len(authors))+ ", "+str(authors))

for i in range(10):
	paper = table_papers.Table_papers(title=titles[i], authors=authors[i])
	paper.insert()

