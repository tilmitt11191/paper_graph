
# -*- coding: utf-8 -*-

import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from log import Log as l
log = l().getLogger()

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
import mysql_operator
from table_papers import Table_papers
from table_citations import Table_citations
db = mysql_operator.Mysql_operator()

paper_records = db.session.query(Table_papers).all()
print("paper_records[" + str(len(paper_records)) + "]")

for start_paper in paper_records:
	for end_paper in paper_records:
		if start_paper.id != end_paper.id:
			print("create cite from[" + str(start_paper.id) + "] to [" + str(end_paper.id) + "]")
			citation = Table_citations(start=start_paper.id, end=end_paper.id)
			citation.renewal_insert()

