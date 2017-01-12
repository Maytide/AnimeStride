import os.path
import sqlite3
import pandas as pd
import numpy as np
# http://stackoverflow.com/questions/305378/list-of-tables-db-schema-dump-etc-using-the-python-sqlite3-api/33100538#33100538

def create_ratings_dataframe(c_u, c_a, verbose = False, max_users = 10000):
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

    # Get all users and their ratings
    # conn_u = sqlite3.connect(user_list_db)
    # c_u = conn_u.cursor()
    c_u.execute('''SELECT name FROM sqlite_master WHERE type="table";''')
    # print(c.fetchall())

    # Get all shows
    # conn_a = sqlite3.connect(show_list_db)
    # c_a = conn_a.cursor()
    c_a.execute('''SELECT * FROM content_data''')

    show_name_list = tuple([item[0] for item in c_a.fetchall()])
    user_ratings_table_list = [item[0] for item in c_u.fetchall()]
    ratings_dataframe = pd.DataFrame()
    users = dict()
    shows = dict()
    show_index = 1
    user_index = 1

    # Select anime, add to dataframe if the anime exists in the content_data (show list) table.
    # TODO: (DONE)
    # Only add shows not rated 0, or -, AND:
    # Only add top 2000 most popular shows
    # Reminder: Temporary table, do not commit anything!
    i = 0
    for user_ratings_table in user_ratings_table_list:
        # user_ratings_dataframe = pd.read_sql('''SELECT "anime","score" FROM "{}" WHERE "score" NOT IN ("0","-")'''.format(user_ratings_table), conn_u)
        user_ratings_dataframe = pd.read_sql('''SELECT "{}" AS user, "anime", "score" FROM "{}"
                                                WHERE ("score" NOT IN ("0","-")
                                                AND "anime" IN {} )'''.format(user_ratings_table, user_ratings_table, show_name_list), conn_u)

        # user_ratings_dataframe = pd.read_sql('''SELECT "{}" AS user, "anime", "score" FROM "{}"
        #                                         WHERE ("score" NOT IN ("0","-"))'''.format(user_ratings_table, user_ratings_table), conn_u)

        for index, row in enumerate(user_ratings_dataframe.itertuples()):
            row_anime = getattr(row, 'anime')
            if row_anime in shows:
                user_ratings_dataframe.set_value(index, 'anime', shows[row_anime])
            elif row_anime not in shows:
                shows[row_anime] = show_index
                user_ratings_dataframe.set_value(index, 'anime', shows[row_anime])
                show_index = show_index + 1

            row_user = getattr(row, 'user')
            if row_user in users:
                user_ratings_dataframe.set_value(index, 'user', users[row_user])
            elif row_user not in users:
                users[row_user] = user_index
                user_ratings_dataframe.set_value(index, 'user', users[row_user])
                user_index = user_index + 1
            pass

        ratings_dataframe = ratings_dataframe.append(user_ratings_dataframe, ignore_index=True)
        if i >= max_users - 2:
            if verbose:
                print('Users: ' + str(user_index) + ', Shows: ' + str(show_index))
                print('Length of dataframe: ' + str(len(ratings_dataframe)))
            break
        if verbose:
            print('user: ' + str(i) + ', ' + user_ratings_table)
        i += 1

    if verbose:
        print('Users: ' + str(user_index) + ', Shows: ' + str(show_index))
        print('Length of dataframe: ' + str(len(ratings_dataframe)))
    # for index, row in enumerate(ratings_dataframe.values):
    #     if index > max_users:
    #         break
    #     print(row)
    # print(ratings_dataframe)
    # print(users)
    # print(shows)
    return (ratings_dataframe,{index: show for show, index in shows.items()} ,{index: user for user, index in users.items()})

def create_ratings_matrix(c_u, c_a, verbose = False, max_users = 10000):
    # conn_u = sqlite3.connect(user_list_db)
    # c_u = conn_u.cursor()
    c_u.execute('''SELECT name FROM sqlite_master WHERE type="table";''')
    # print(c.fetchall())

    # Get all shows
    # conn_a = sqlite3.connect(show_list_db)
    # c_a = conn_a.cursor()
    c_a.execute('''SELECT * FROM content_data''')

    show_name_list = tuple([item[0] for item in c_a.fetchall()])
    user_ratings_table_list = [item[0] for item in c_u.fetchall()]
    users = dict()
    shows = dict()
    num_users = max_users
    num_shows = len(show_name_list)

    for index, show in enumerate(show_name_list):
        shows[show] = index + 1

    ratings_matrix = np.zeros((num_shows, num_users))
    if verbose:
        print(ratings_matrix.shape)
    show_index = 1
    user_index = 1



    # Future possible change ?:
    # http://stackoverflow.com/questions/29582736/python3-is-there-a-way-to-iterate-row-by-row-over-a-very-large-sqlite-table-wi
    i = 0
    for user_ratings_table in user_ratings_table_list:
        if i > num_users - 2:
            break
        c_u.execute('''SELECT "{}" AS user, "anime", "score" FROM "{}"
                       WHERE ("score" NOT IN ("0","-")
                       AND "anime" IN {} )'''.format(user_ratings_table, user_ratings_table, show_name_list))

        index = 0
        for row_user, row_anime, score in c_u:

            # if row_anime not in shows:
            #     shows[row_anime] = show_index
            #     show_index = show_index + 1

            if row_user not in users:
                users[row_user] = user_index
                user_index = user_index + 1
                i = i + 1

            # print(i, row_user, users[row_user])
            ratings_matrix[shows[row_anime]][users[row_user]] = score
            # if row_anime in shows:
            #     ratings_matrix[shows[row_anime]][users[row_user]] = score
            # elif row_anime not in shows:
            #     shows[row_anime] = show_index
            #     ratings_matrix[shows[row_anime]][users[row_user]] = score
            #     show_index = show_index + 1
            #
            # if row_user in users:
            #     ratings_matrix[shows[row_anime]][users[row_user]] = score
            # elif row_user not in users:
            #     users[row_user] = user_index
            #     ratings_matrix[shows[row_anime]][users[row_user]] = score
            #     user_index = user_index + 1
            # index += 1
        if verbose:
            print('user: ' + str(i) + ', ' + user_ratings_table)


    if verbose:
        print('Users: ' + str(user_index) + ', Shows: ' + str(show_index))
        print('Matrix Dimensions: ' + str(ratings_matrix.shape))


    return (num_shows, ratings_matrix, shows, users)
# print(create_ratings_dataframe(max_users=1))

# def index_dataframe(dataframe):
#     indexed_dataframe = pd.DataFrame()

# def read_data_from_db(db = 'sample_user_list.db'):
#     users_db = db
#     conn = sqlite3.connect(db)
#     c = conn.cursor()
#
#     c.execute('SELECT * FROM big_table')
#     for row in c:
#         pass


# db = dirname(dirname(__file__)) +'/data/' + 'sample_user_list.db'
# user_list_db = 'sample_user_list.db'
# show_list_db = 'show_data.db'
# create_ratings_dataframe(user_list_db, show_list_db).to_csv('sample_user_csv.txt', sep='\t', encoding='utf-8')