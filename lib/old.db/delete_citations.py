
# -*- coding: utf-8 -*-

print("delete citations ok? [y/n]")
arg = input()


import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from log import Log as l
log = l().getLogger()

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
import mysql_operator
from table_citations import Table_citations
db = mysql_operator.Mysql_operator()

if arg == "y":
	db.session.query(Table_citations).delete()
	db.session.commit()

