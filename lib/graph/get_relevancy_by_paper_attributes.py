
# -*- coding: utf-8 -*-

points_per_keyword = 2
points_per_author = 4
points_per_citing = 5
points_per_cited = 5
points_per_conference = 1
points_per_published = 0

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from log import Log as l

log = l.getLogger()
log.info("get_papers_at_frist_keywords_next_citings.py start.")


sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
import mysql_operator
from table_papers import Table_papers
from table_citations import Table_citations
from table_edges import Table_edges

db = mysql_operator.Mysql_operator()
papers = db.session.query(Table_papers).all()
citations = db.session.query(Table_citations).all()
db.session.query(Table_edges).delete()
db.session.commit()
edges = []
def already_registered(start, end):
	for edge in edges:
		if edge.start == start and edge.end == end:
			return True
	return False

def shared_keyword_check(start_paper, end_paper):
	relevancy = 0
	start_keywords = start_paper.keywords.split(",")
	end_keywords = end_paper.keywords.split(",")
	for keyword in start_keywords:
		if keyword in end_keywords and keyword != "":
			relevancy += points_per_keyword
	return relevancy

def shared_author_check(start_paper, end_paper):
	relevancy = 0
	start_authors = start_paper.authors.split(",")
	end_authors = end_paper.authors.split(",")
	for author in start_authors:
		if author in end_authors and author != "":
			relevancy += points_per_author
	return relevancy

def citing_check(start_paper, end_paper):
	for citation in citations:
		if citation.start == start_paper.id and citation.end == end_paper.id:
			return points_per_citing
	return 0
	
def cited_check(start_paper, end_paper):
	for citation in citations:
		if citation.start == end_paper.id and citation.end == start_paper.id:
			return points_per_cited
	return 0

def check_conference(start_paper, end_paper):
	if start_paper.conference != "" and start_paper.conference == end_paper.conference:
		return points_per_conference
	return 0

def check_published(start_paper, end_paper):
	if start_paper.published != None and start_paper.published == end_paper.published:
		return points_per_published
	return 0

for start_paper in papers:
	for end_paper in papers:
		if start_paper.id == end_paper.id:
			continue
		if already_registered(start=end_paper.id, end = start_paper.id):
			continue
		relevancy = 0
		print("start[" + str(start_paper.id) + "], end[" + str(end_paper.id) + "]")
		#print("relevancy[" + str(relevancy) + "]")
		relevancy += shared_keyword_check(start_paper, end_paper)
		#print("relevancy[" + str(relevancy) + "]")
		relevancy += shared_author_check(start_paper, end_paper)
		#print("relevancy[" + str(relevancy) + "]")
		relevancy += citing_check(start_paper, end_paper)
		#print("relevancy[" + str(relevancy) + "]")
		relevancy += cited_check(start_paper, end_paper)
		#print("relevancy[" + str(relevancy) + "]")
		relevancy += check_conference(start_paper, end_paper)
		#print("relevancy[" + str(relevancy) + "]")
		relevancy += check_published(start_paper, end_paper)
		print("relevancy[" + str(relevancy) + "]")
		
		if relevancy != 0:
			edge = Table_edges(start=start_paper.id, end=end_paper.id, relevancy=relevancy)
			edges.append(edge)
			edge.insert()
			edge.db.close()


