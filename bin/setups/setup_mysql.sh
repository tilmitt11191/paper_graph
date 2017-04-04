
# -*- coding: utf-8 -*-

USER="alladmin"

mysql -u root -p -e "\
create user 'alladmin'@'localhost' identified by 'admin';\
create database paper_graph;\
grant ALL on paper_graph.* to 'alladmin'@'localhost'; 
create table paper_graph.papers (\
id int, \
title text, \
authors tinytext, \
keywords tinytext, \
cites tinytext, \
path tinytext, \
timestamp DATETIME);\
flush privileges;"