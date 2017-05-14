
# -*- coding: utf-8 -*-


#sudo apt-get -y install mysql-server

#sudo mysql -p -e "\
#drop user 'alladmin'@'localhost';\
#flush privileges;"

echo "create user 'alladmin'@'localhost'"
sudo mysql -p -e "\
create user 'alladmin'@'localhost' identified by 'admin';\
flush privileges;"

echo "drop database paper_graph"
sudo mysql -p -e "\
drop database paper_graph;\
create database paper_graph;\
grant ALL on paper_graph.* to 'alladmin'@'localhost';\
flush privileges;"

echo "create table paper_graph.papers"
sudo mysql -p -e "\
create table paper_graph.papers (\
id int, \
title text, \
authors text, \
keywords text, \
citings mediumtext, \
citeds mediumtext, \
conference tinytext, \
published DATE, \
url tinytext, \
abstract_path text, \
pdf_path text, \
timestamp DATETIME, \
label tinytext, \
color tinytext);\
alter table paper_graph.papers default character set "utf8";\
flush privileges;"

echo "create table paper_graph.citations"
sudo mysql -p -e "\
create table paper_graph.citations (\
id int, \
start int, \
end int);\
flush privileges;"


echo "create table paper_graph.authors"
sudo mysql -p -e "\
create table paper_graph.authors (\
id int, \
name tinytext, \
belonging tinytext);\
flush privileges;"


echo "create table paper_graph.edges"
sudo mysql -p -e "\
create table paper_graph.edges (\
id int, \
start int, \
end int, \
relevancy float);\
flush privileges;"

#id int NOT NULL PRIMARY KEY
