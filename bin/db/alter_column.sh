

#ALTER TABLE tbl_name CHANGE [COLUMN] old_col_name column_definition;
sudo mysql -p -e "\
alter table paper_graph.papers change path path text;\
flush privileges;"
