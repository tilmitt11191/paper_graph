
# -*- coding: utf-8 -*-


#sudo apt-get -y install mysql-server

sudo mysql -p -e "\
drop user 'alladmin'@'localhost';\
flush privileges;"

sudo mysql -p -e "\
create user 'alladmin'@'localhost' identified by 'admin';\
flush privileges;"

sudo mysql -p -e "\
drop database paper_graph;\
flush privileges;"

sudo mysql -p -e "\
create database paper_graph;\
grant ALL on paper_graph.* to 'alladmin'@'localhost';\
create table paper_graph.papers (\
id int, \
title text, \
authors text, \
keywords text, \
citings tinytext, \
citeds tinytext, \
conference tinytext, \
published DATE, \
url tinytext, \
timestamp DATETIME, \
path tinytext, \
label tinytext, \
color tinytext);\
alter table papers default character set "utf8";\
flush privileges;"

sudo mysql -p -e "\
create table paper_graph.citations (\
id int, \
start int, \
end int);\
flush privileges;"

sudo mysql -p -e "\
create table paper_graph.edges (\
id int, \
start int, \
end int, \
relevancy float);\
flush privileges;"

#id int NOT NULL PRIMARY KEY
