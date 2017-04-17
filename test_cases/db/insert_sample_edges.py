
# -*- coding: utf-8 -*-

import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from log import Log as l
log = l().getLogger()

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
import mysql_operator
import table_edges
db = mysql_operator.Mysql_operator()

i = 1

for start in range(10):
	for end in range(10):
		if start != end:
			edge = table_edges.Table_edges(id=i, start=start+1, end=end+1, relevancy=start*end)
			db.insert(edge)
			i+=1

