  387  mysqldump -u 'alladmin' -p -h 'localhost' 'paper_graph' 'papers' > mysqldump_papers_242
	  388  mysqldump -u 'alladmin' -p -h 'localhost' 'paper_graph' 'citations' > mysqldump_citations_242
		  389  mysqldump -u 'alladmin' -p -h 'localhost' 'paper_graph' 'edges' > mysqldump_edge_242

mysql -u 'alladmin' -p -h 'localhost' 'paper_graph' < ../workspace/mysqldump_papers_242 
  125  mysql -u 'alladmin' -p -h 'localhost' 'paper_graph' < ../workspace/mysqldump_citations_242
	  126  mysql -u 'alladmin' -p -h 'localhost' 'paper_graph' < ../workspace/mysqldump_edge_242

