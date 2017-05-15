In order for program to work, file should contain 4 SQLite databases:

show_data_individual.db     Database of show statistics over time, where each show is a table;
show_data_aggregated.db     Database of all show information, where each show is a row in the table (tables content_data, basic_statistics and item_recs)
user_list_indexed.sqlite3	Database of users and their watched shows, where each user is a table;
show_indices.db         	Database of the indexing scheme used to store each user's shows.



