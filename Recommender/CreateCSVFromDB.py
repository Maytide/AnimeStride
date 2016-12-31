import os.path
import sqlite3
import pandas as pd
# http://stackoverflow.com/questions/305378/list-of-tables-db-schema-dump-etc-using-the-python-sqlite3-api/33100538#33100538

def create_ratings_dataframe(user_list_db ='sample_user_list.db', show_list_db = 'show_data.db'):
    # conn = sqlite3.connect(db)
    # c = conn.cursor()
    # c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # tables = c.fetchall()
    # for table_name in tables:
    #     table_name = table_name[0]
    #     print(table_name)
    #     table = pd.read_sql_query("SELECT * from %s" % table_name, db)
    #     table.to_csv(table_name + '.csv', index_label='index')

    # http://stackoverflow.com/questions/167576/check-if-table-exists-in-sql-server
    # http://stackoverflow.com/questions/24408557/pandas-read-sql-with-parameters
    # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_sql_table.html#pandas.read_sql_table


    conn_u = sqlite3.connect(user_list_db)
    c_u = conn_u.cursor()
    c_u.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(c.fetchall())

    conn_a = sqlite3.connect(show_list_db)
    c_a = conn_a.cursor()


    for ratings_table, none in c_u.fetchall():
        # Select anime, add to dataframe if the anime exists in the content_data (show list) table.
        ratings_dataframe = pd.read_sql('''SELECT "anime","score" FROM "{}"'''.format(ratings_table))

# def read_data_from_db(db = 'sample_user_list.db'):
#     users_db = db
#     conn = sqlite3.connect(db)
#     c = conn.cursor()
#
#     c.execute('SELECT * FROM big_table')
#     for row in c:
#         pass


# db = dirname(dirname(__file__)) +'/data/' + 'sample_user_list.db'
user_list_db = 'sample_user_list.db'
show_list_db = 'show_data.db'
create_ratings_dataframe(user_list_db, show_list_db)