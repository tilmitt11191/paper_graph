
# -*- coding: utf-8 -*-

USER="alladmin"


#sudo mysql -p -e "\
#create user 'alladmin'@'localhost' identified by 'admin';\
#flush privileges;"

sudo mysql -p -e "\
create database paper_graph;\
grant ALL on paper_graph.* to '$USER'@'localhost';\
create table paper_graph.papers (\
id int, \
title text, \
authors tinytext, \
keywords tinytext, \
cites tinytext, \
path tinytext, \
timestamp DATETIME, \
is_cached boolean);\
flush privileges;"


#mysql -u root -p -e "\
#drop database paper_graph;
