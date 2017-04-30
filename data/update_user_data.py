from collections import OrderedDict
import time

import sqlite3
from urllib.error import HTTPError as HTTPError

from master import UNMODELED_DATABASES, escape_db_string, unescape_db_string
from data.open_db import open_db
from User import User

# master_dict_n, master_map, show_map, user_rating_table_list

# 169
def update_user_data(verbose=False, start_point=0, max_users=10000):
    item_dict = open_db(max_users, 1, open_show_indices=True, open_show_data_aggregated=False, open_user_list_indexed=True, get_conn_n=True, get_conn_x=True)
    print('Update_user_data: length of master_map', len(item_dict['master_map']))
    # print(item_dict['user_rating_table_list'])
    init_show_map_len = item_dict['master_map_max']

    c_x = item_dict['conn_x'].cursor()
    c_n = item_dict['conn_n'].cursor()

    i = start_point
    cre_count = 0
    for user_rating_table in item_dict['user_rating_table_list'][start_point:]:
        if verbose:
            print(str(i)+':', 'Parsing entries for user: ' + user_rating_table)
            i += 1

        try:
            user = User()
            user.MAL_URL = user_rating_table
            user.create_user_show_list_tagged(user_rating_table, minimal=True)
        except HTTPError:
            print('HTTPError for user', user_rating_table)
            continue
        except ConnectionResetError as ex:
            print('ConnectionResetError for user', user_rating_table, ex)
            cre_count += 1
            if cre_count < 5:
                time.sleep(60)
            elif cre_count < 6:
                print('Five ConnectionResetErrors have occured -- something is probably wrong.')
                time.sleep(300)
            else:
                print('Six ConnectionResetErrors have occured -- aborting task.')
                break
            continue
        # print(user.entry_list_tagged)
        try:
            init_show_map_len = item_dict['master_map_max']
            for score_data, title_data in user.entry_list_tagged:
                score_data = score_data[1]
                title_data = title_data[1]


                if score_data == '-':
                    score_data = 0
                else:
                    try:
                        score_data = int(score_data)
                    except Exception as ex:
                        print('Exception for user ' + str(user), title_data, score_data, ex)
                        score_data = 0

                if title_data in item_dict['master_dict_n'] or unescape_db_string(title_data) in item_dict[
                    'master_dict_n']:
                    title_index = item_dict['master_dict_n'][title_data]
                else:
                    # curr_len = item_dict['master_map_max']
                    # item_dict['master_dict_n'][title_data] = curr_len
                    # item_dict['master_map'][curr_len] = title_data
                    # item_dict['master_map_max'] = item_dict['master_map_max'] + 1
                    #
                    # title_index = item_dict['master_dict_n'][title_data]
                    # if verbose:
                    #     print('Added show', title_data, 'to master_map and master_dict')
                    #     # print('Master Dict now has size', len(item_dict['master_dict_n']))
                    #     # print('Master Map now has size', len(item_dict['master_map']))
                    #     # print(title_data, score_data)
                    #     # print(title_index, score_data)
                    #     print('Assigning show', title_data, 'to master_dict id', item_dict['master_dict_n'][title_data])
                    #
                    #     print()
                    # c_n.execute('''INSERT OR REPLACE INTO show_map VALUES (?,?)''',
                    #             (item_dict['master_map'][curr_len], curr_len))
                    pass


                c_x.execute('''INSERT OR REPLACE INTO [{}]
                                   VALUES (?,?)'''.format(user_rating_table), (title_index, score_data))

                # IF loop is executed unto completion, success is true
                pass
            item_dict['conn_n'].commit()
            item_dict['conn_x'].commit()

        except ValueError as ve:
            print('ValueError for user ' + str(user), ve)
            pass
        except Exception as ex:
            print('Unknown Exception for user ' + str(user), ex)
            pass

    # for show_id in range(init_show_map_len, len(item_dict['master_map'])):
    #     c_n.execute('''INSERT OR REPLACE INTO show_map
    #                 VALUES (?,?)''', (item_dict['master_map'][show_id], show_id))
        # print(item_dict['master_map'][show_id], show_id)

    item_dict['conn_x'].commit()
    item_dict['conn_n'].commit()
    item_dict['conn_x'].close()
    item_dict['conn_n'].close()




# update_user_data(verbose=True, start_point=4660)