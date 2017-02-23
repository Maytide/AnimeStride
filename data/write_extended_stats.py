from math import sqrt
from collections import OrderedDict

import sqlite3
import numpy as np

from master import UNMODELED_DATABASES, escape_db_string, unescape_db_string

def open_db(max_users, max_shows):
    db_n = UNMODELED_DATABASES['show_indices']['location']
    conn_n = sqlite3.connect(db_n)
    c_n = conn_n.cursor()

    c_n.execute('''SELECT * FROM show_map
                    ''')
    master_dict_n = {name: index for name, index in c_n.fetchall()}
    master_map = {index: name for name, index in master_dict_n.items()}

    conn_n.close()

    ############################################

    db_a = UNMODELED_DATABASES['show_data_aggregated']['location']
    conn_a = sqlite3.connect(db_a)
    c_a = conn_a.cursor()

    c_a.execute('''SELECT name FROM content_data ORDER BY popularity LIMIT (?)''', (max_shows,))

    raw_data = c_a.fetchall()

    show_map = {index: name[0] for index, name in enumerate(raw_data)}
    show_dict = {name: index for index, name in show_map.items()}

    # master_stat_dict = {index: {'rating_hist': np.zeros(11), 'var': -1, 'mean': -1, 'std': -1} for name, index in
    #                     show_dict.items()}

    conn_a.close()

    ############################################

    db_x = 'user_list_indexed.sqlite3'
    conn_x = sqlite3.connect(db_x)
    c_x = conn_x.cursor()

    c_x.execute('''SELECT tbl_name FROM sqlite_master WHERE type="table"
                LIMIT (?);''', (max_users,))

    user_rating_table_list = [item[0] for item in c_x.fetchall()]

    return conn_x, master_dict_n, master_map, show_dict, show_map, user_rating_table_list
    ############################################


def write_extended_stats(max_users, max_shows, basic_statistics=True, item_rec=True):
    conn_x, master_dict_n, master_map, show_dict, show_map, user_rating_table_list = open_db(max_users, max_shows)
    c_x = conn_x.cursor()
    master_stat_dict = calculate_basic_statistics(c_x, max_users, max_shows, master_dict_n, master_map, show_dict, show_map, user_rating_table_list)

    calculate_corr_statistics(c_x, max_users, max_shows, master_dict_n, master_map, show_dict, show_map, user_rating_table_list)
    # print(master_stat_dict[master_dict_n['Rokka no Yuusha']]['rating_hist'])
    # print(master_stat_dict[master_dict_n['Rokka no Yuusha']])
    # print(master_stat_dict[master_dict_n['Sword Art Online']])
    # print(master_stat_dict[master_dict_n['Fullmetal Alchemist: Brotherhood']])


    # print('Hello')


    conn_x.close()


def a_cos_sim(v1, v2, mu, threshold=100, correction_fact=0.98):

    num = 0
    den_v1 = 0
    den_v2 = 0
    num_common = 0

    i = 0
    for r1, r2 in zip(v1, v2):
        if r1 > 0 and r2 > 0:
            v1_reg = v1[i] - mu[i]
            v2_reg = v2[i] - mu[i]

            num += v1_reg * v2_reg
            den_v1 += v1_reg * v1_reg
            den_v2 += v2_reg * v2_reg

            num_common += 1

        i += 1

    if num_common == 0:
        return 0

    # threshold = 100
    if num_common > threshold:
        correction = 1
    else:
        correction = correction_fact ** (threshold - num_common)

    a_cos = correction * num / sqrt(den_v1 * den_v2)

    return a_cos


def calculate_corr_statistics(c_x, max_users, max_shows, master_dict_n, master_map, show_dict, show_map, user_rating_table_list, num_recs=6):
    A = np.zeros((max_shows, max_users))
    user_mean_list = np.zeros(max_users)


    u = 0
    for index_u, user_rating_table_2 in enumerate(user_rating_table_list):
        print(index_u, 'Reading ratings for: ', user_rating_table_2)
        c_x.execute('SELECT show, rating FROM [{urt}]'.format(urt=user_rating_table_2))

        user_rating_list = c_x.fetchall()

        user_mean_i = 0
        num_ratings_i = 0
        for show_code, rating in user_rating_list:
            if rating > 0:
                user_mean_i += rating
                num_ratings_i += 1

                # print(show_code)
                # print(master_map[show_code])
            if show_code in master_map and master_map[show_code] in show_dict:
                A[show_dict[master_map[show_code]], u] = rating
                # if show_code not in show_stat_dict:
                #     show_stat_dict[show_code] = {'rating_hist': np.zeros(11), 'var': -1, 'mean': -1, 'std': -1}
                # show_stat_dict[show_code]['rating_hist'][rating] += 1

        num_ratings_i = num_ratings_i if num_ratings_i > 0 else 1

        user_mean_i /= num_ratings_i
        user_mean_list[index_u] = user_mean_i
        # user_rating_list_list.append(user_rating_list)
        u += 1



    C = np.zeros((max_shows, max_shows))
    max_a_cos = np.zeros((max_shows, num_recs)) - 1
    max_a_cos_index = np.zeros((max_shows, num_recs))

    for index_i, row in enumerate(A):
        for index_j in range(index_i, max_shows):
            C[index_i, index_j] = a_cos_sim(A[index_i, :], A[index_j, :], user_mean_list)
            C[index_j, index_i] = C[index_i, index_j]

    for index_i in range(max_shows):
        for index_j in range(max_shows):

            if index_i != index_j and C[index_i, index_j] > max_a_cos[index_i, num_recs - 1]:
                max_a_cos[index_i, num_recs - 1] = C[index_i, index_j]
                max_a_cos_index[index_i, num_recs - 1] = index_j
                for r in range(num_recs - 2, -1, -1):
                    if max_a_cos[index_i, r + 1] > max_a_cos[index_i, r]:
                        max_a_cos[index_i, r], max_a_cos[index_i, r + 1] = max_a_cos[index_i, r + 1], \
                                                                           max_a_cos[index_i, r]
                        max_a_cos_index[index_i, r], max_a_cos_index[index_i, r + 1] = max_a_cos_index[index_i, r + 1], \
                                                                                       max_a_cos_index[index_i, r]
                    else:
                        break

    avg_corr = []
    for index in range(max_shows):
        avg_i = np.mean(C[index])
        avg_corr.append(avg_i)
        print(index, 'Average correlation for show:', show_map[index], avg_i)

    master_rec_dict = {}
    tl_rec_dict = {}

    for index, rec_list in enumerate(max_a_cos_index):

        show_rec = []
        show_rec_tl = []
        for rec in rec_list:
            # show_rec.append(show_map[rec])
            show_rec_tl.append(show_map[rec])
            show_rec.append(master_dict_n[escape_db_string(show_map[rec])])
            # show_rec.append(master_dict_n[escape_db_string(show_map[rec])])

        # master_rec_list.append(show_rec)
        print(show_map[index])
        print(master_dict_n[escape_db_string(show_map[index])])
        master_rec_dict[master_dict_n[escape_db_string(show_map[index])]] = show_rec
        tl_rec_dict[show_map[index]] = show_rec_tl


        # print('Recommendation for show: ' + show_map[index])
        #
        # print(show_rec)
        # print('Corr scores:', max_a_cos[index])

    print(master_rec_dict)
    print(tl_rec_dict)

    # return master_rec_list


def calculate_basic_statistics(c_x, max_users, max_shows, master_dict_n, master_map, show_dict, show_map, user_rating_table_list):
    # print(master_stat_dict)
    master_stat_dict = OrderedDict()

    for user_rating_table in user_rating_table_list:
        print('Reading ratings for: ', user_rating_table)
        c_x.execute('SELECT show, rating FROM [{urt}]'.format(urt=user_rating_table))

        for show_code, rating in c_x.fetchall():
            if show_code in master_map and unescape_db_string(master_map[show_code]) in show_dict:
                if show_code not in master_stat_dict:
                    master_stat_dict[show_code] = {'rating_hist': np.zeros(11), 'var': -1, 'mean': -1, 'std': -1}
                master_stat_dict[show_code]['rating_hist'][rating] += 1

    # print(master_stat_dict[master_dict_n['Sword Art Online']]['rating_hist'])
    # print(master_stat_dict[master_dict_n['Rokka no Yuusha']]['rating_hist'])

    for show_code, info in master_stat_dict.items():
        mean = 0
        var = 0
        num_ratings = 0
        for rating, num_ratings_i in enumerate(master_stat_dict[show_code]['rating_hist']):
            if rating != 0:
                mean += rating * num_ratings_i
                num_ratings += num_ratings_i

        num_ratings = num_ratings if num_ratings != 0 else 1
        mean /= num_ratings

        master_stat_dict[show_code]['mean'] = mean

        for rating, num_ratings_i in enumerate(master_stat_dict[show_code]['rating_hist']):
            if rating != 0:
                var += num_ratings_i * (mean - rating) * (mean - rating)

        num_ratings = num_ratings if num_ratings > 1 else 2
        var /= (num_ratings - 1)
        std = sqrt(var)

        master_stat_dict[show_code]['var'] = var
        master_stat_dict[show_code]['std'] = std

        # print('Mean for show', master_map[show], ': ', mean)
        # print('Variance for show', master_map[show], ': ', var)
        # print('Std deviation for show', master_map[show], ': ', std)
        # print()

        # print('Stats for show', master_map[show_code])
        # print(master_stat_dict[show_code]['rating_hist'])
        # print('mean:', master_stat_dict[show_code]['mean'])
        # print('variance', master_stat_dict[show_code]['var'])
        # print('Num ratings:', np.sum(master_stat_dict[show_code]['rating_hist'][1:]))
        # print()

    return master_stat_dict

max_users = 1000
max_shows = 200

write_extended_stats(max_users, max_shows, item_rec=False)