from collections import OrderedDict

import sqlite3

from master import UNMODELED_DATABASES, escape_db_string, unescape_db_string


def open_db(max_users, max_shows, open_show_indices=True, open_show_data_aggregated=True, open_user_list_indexed=True, get_conn_n=False, get_conn_x=False):
    item_dict = dict()

    if open_show_indices:
        db_n = UNMODELED_DATABASES['show_indices']['location']
        conn_n = sqlite3.connect(db_n)
        c_n = conn_n.cursor()

        c_n.execute('''SELECT * FROM show_map
                        ''')

        master_dict_n = dict()
        max_index = 0
        for name, index in c_n.fetchall():
            master_dict_n[name] = index
            if index > max_index:
                max_index = index

        # VERY important
        max_index = max_index + 1

        # master_dict_n = {name: index for name, index in c_n.fetchall()}
        master_map = {index: name for name, index in master_dict_n.items()}

        item_dict['master_dict_n'] = master_dict_n
        item_dict['master_map'] = master_map
        item_dict['master_map_max'] = max_index

        if get_conn_n:
            item_dict['conn_n'] = conn_n
        else:
            conn_n.close()

    ############################################

    if open_show_data_aggregated:
        db_a = UNMODELED_DATABASES['show_data_aggregated']['location']
        conn_a = sqlite3.connect(db_a)
        c_a = conn_a.cursor()

        c_a.execute('''SELECT name FROM content_data ORDER BY popularity LIMIT (?)''', (max_shows,))

        raw_data = c_a.fetchall()

        show_map = {index: name[0] for index, name in enumerate(raw_data)}
        show_dict = {name: index for index, name in show_map.items()}

        item_dict['show_map'] = show_map
        item_dict['show_dict'] = show_dict

        conn_a.close()

    ############################################
    if open_user_list_indexed:
        db_x = UNMODELED_DATABASES['user_list_indexed']['location']
        conn_x = sqlite3.connect(db_x)
        c_x = conn_x.cursor()

        c_x.execute('''SELECT tbl_name FROM sqlite_master WHERE type="table"
                    LIMIT (?);''', (max_users,))

        user_rating_table_list = [item[0] for item in c_x.fetchall()]

        item_dict['user_rating_table_list'] = user_rating_table_list

        if get_conn_x:
            item_dict['conn_x'] = conn_x
        else:
            conn_x.close()



    return item_dict