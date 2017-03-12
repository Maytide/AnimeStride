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

    db_x = UNMODELED_DATABASES['user_list_indexed']['location']
    conn_x = sqlite3.connect(db_x)
    c_x = conn_x.cursor()

    c_x.execute('''SELECT tbl_name FROM sqlite_master WHERE type="table"
                LIMIT (?);''', (max_users,))

    user_rating_table_list = [item[0] for item in c_x.fetchall()]

    return conn_x, master_dict_n, master_map, show_dict, show_map, user_rating_table_list
    ############################################


def write_extended_stats(max_users, max_shows, basic_statistics=False, item_rec=False, verbose=False):
    conn_x, master_dict_n, master_map, show_dict, show_map, user_rating_table_list = open_db(max_users, max_shows)
    c_x = conn_x.cursor()

    master_stat_dict = calculate_basic_statistics(c_x, max_users, max_shows, master_dict_n, master_map, show_dict, show_map, user_rating_table_list, verbose=verbose)

    rec_dict = None
    if item_rec:
        rec_dict = calculate_corr_statistics(c_x, max_users, max_shows, master_dict_n, master_map, show_dict, show_map, user_rating_table_list, master_stat_dict, verbose=verbose)
    # print(master_stat_dict[master_dict_n['Rokka no Yuusha']]['rating_hist'])
    # print(master_stat_dict[master_dict_n['Rokka no Yuusha']])
    # print(master_stat_dict[master_dict_n['Sword Art Online']])
    # print(master_stat_dict[master_dict_n['Fullmetal Alchemist: Brotherhood']])
    # print('Hello')
    conn_x.close()

    # print(master_stat_dict[master_dict_n['Rokka no Yuusha']]['mean'])
    #
    # print(master_stat_dict)
    # print(rec_dict)

    db_s = UNMODELED_DATABASES['show_data_aggregated']['location']
    conn_s = sqlite3.connect(db_s)
    c_s = conn_s.cursor()


    if basic_statistics:
        if verbose:
            print('Writing basic statistic data to database...')
        c_s.execute('''CREATE TABLE IF NOT EXISTS basic_statistics
                    (show_code TEXT PRIMARY KEY, mean REAL, var REAL, std REAL,
                    rating_zero INTEGER, rating_one INTEGER, rating_two INTEGER, rating_three INTEGER, rating_four INTEGER, rating_five INTEGER,
                    rating_six INTEGER, rating_seven INTEGER, rating_eight INTEGER, rating_nine INTEGER, rating_ten INTEGER,
                    extra_1 INTEGER, extra_2 INTEGER)''')

        for show_code, info in master_stat_dict.items():

            c_s.execute('''INSERT OR REPLACE INTO basic_statistics VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        ''', (unescape_db_string(master_map[show_code]), info['mean'], info['var'], info['std'],
                              info['rating_hist'][0], info['rating_hist'][1], info['rating_hist'][2], info['rating_hist'][3],
                              info['rating_hist'][4], info['rating_hist'][5], info['rating_hist'][6], info['rating_hist'][7],
                              info['rating_hist'][8], info['rating_hist'][9], info['rating_hist'][10], 0, 0))

    if item_rec:
        if verbose:
            print('Writing item recommendation data to database...')

        c_s.execute('''CREATE TABLE IF NOT EXISTS item_recs
                    (show_code TEXT PRIMARY KEY,
                    rec_1 TEXT, rec_2 TEXT, rec_3 TEXT, rec_4 TEXT, rec_5 TEXT, rec_6 TEXT)''')

        for show_code, show_rec_list in rec_dict.items():

            c_s.execute('''INSERT OR REPLACE INTO item_recs VALUES (?,?,?,?,?,?,?)
                        ''', (unescape_db_string(master_map[show_code]),) + tuple([unescape_db_string(master_map[show]) for show in show_rec_list]))

        pass


    conn_s.commit()
    conn_s.close()


def a_cos_sim(v1, v2, mu, threshold=200, correction_fact=0.995, mean1=-1, mean2=-1, var1=-1, var2=-1):

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
    if num_common >= threshold:
        correction = 1
    else:
        correction = correction_fact ** (threshold - num_common)

    if mean1 > 8.3 and mean2 > 8.3 and var1 > 0 and var2 > 0:
        # correction *= 0.2 + 0.8/(1 + 2.7182818 ** (-abs((mean1 - mean2)*(var1 - var2))*20))
        correction = 0
    elif mean2 > 8.3:
        correction *= 0.2

    a_cos = correction * num / sqrt(den_v1 * den_v2)

    return a_cos


def calculate_corr_statistics(c_x, max_users, max_shows, master_dict_n, master_map, show_dict, show_map, user_rating_table_list, master_stat_dict, num_recs=6, verbose=False):
    A = np.zeros((max_shows, max_users))
    user_mean_list = np.zeros(max_users)

    if verbose:
        print('Loading user rating tables into rating matrix...')
    u = 0
    for index_u, user_rating_table_2 in enumerate(user_rating_table_list):
        # print(index_u, 'Reading ratings for: ', user_rating_table_2)
        c_x.execute('SELECT show, rating FROM [{urt}]'.format(urt=user_rating_table_2))

        user_rating_list = c_x.fetchall()

        user_mean_i = 0
        num_ratings_i = 0
        for show_code, rating in user_rating_list:
            if rating > 0:
                user_mean_i += rating
                num_ratings_i += 1

            # if 'Gate: Jieitai' in master_map[show_code]:
            #     print(show_code)
            #     print(master_map[show_code])
            if show_code in master_map and unescape_db_string(master_map[show_code]) in show_dict:
                A[show_dict[unescape_db_string(master_map[show_code])], u] = rating
                # if show_code not in show_stat_dict:
                #     show_stat_dict[show_code] = {'rating_hist': np.zeros(11), 'var': -1, 'mean': -1, 'std': -1}
                # show_stat_dict[show_code]['rating_hist'][rating] += 1

        num_ratings_i = num_ratings_i if num_ratings_i > 0 else 1

        user_mean_i /= num_ratings_i
        user_mean_list[index_u] = user_mean_i
        # user_rating_list_list.append(user_rating_list)
        u += 1

    if verbose:
        print('Rating matrix built.')
        print('Calculating cosine similarities between shows...')

    C = np.zeros((max_shows, max_shows))
    max_a_cos = np.zeros((max_shows, num_recs)) - 1
    max_a_cos_index = np.zeros((max_shows, num_recs))

    for index_i, row in enumerate(A):
        i_show_mean, i_show_var = -1, -1
        if index_i in show_map and show_map[index_i] in master_dict_n:
            i_show = master_dict_n[show_map[index_i]]
            if i_show in master_stat_dict:
                i_show_mean = master_stat_dict[i_show]['mean']
                i_show_var = master_stat_dict[i_show]['var']

        for index_j in range(index_i, max_shows):
            j_show_mean, j_show_var = -1, -1
            if index_j in show_map and show_map[index_j] in master_dict_n:
                j_show = master_dict_n[show_map[index_j]]
                if j_show in master_stat_dict:
                    j_show_mean = master_stat_dict[j_show]['mean']
                    j_show_var = master_stat_dict[j_show]['var']

            C[index_i, index_j] = a_cos_sim(A[index_i, :], A[index_j, :], user_mean_list, mean1 = i_show_mean, mean2 = j_show_mean, var1 = i_show_var, var2 = j_show_var)
            C[index_j, index_i] = C[index_i, index_j]

            # if i_show_mean > 8.3 and j_show_mean > 8.3:
            #     print(show_map[index_i], show_map[index_j])
            #     print(C[index_i, index_j])
            #     print()

        if verbose and index_i % 10 == 0:
            print('Done show', index_i, 'of a possible', max_shows)
            print(i_show, master_map[i_show])

    # for index, row in enumerate(C):
    #     print(index, show_map[index])
    #     # for index, sim in enumerate(C[index]):
    #     #     print(show_map[index], sim, end=', ')
    #     print(row)

    if verbose:
        print('Done calculating all cosine similarities.')
        print('Generating recommendations...')

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

    if verbose:
        print('Done generating recommendations')
        print('Packing recommendations for database...')

    avg_corr = []
    for index in range(max_shows):
        avg_i = np.mean(C[index])
        avg_corr.append(avg_i)
        # print(index, 'Average correlation for show:', show_map[index], avg_i)

    master_rec_dict = {}
    # tl_rec_dict = {}

    for index, rec_list in enumerate(max_a_cos_index):

        show_rec = []
        show_rec_tl = []
        for rec in rec_list:
            # show_rec.append(show_map[rec])
            show_rec_tl.append(show_map[rec])
            show_rec.append(master_dict_n[escape_db_string(show_map[rec])])
            # show_rec.append(master_dict_n[escape_db_string(show_map[rec])])

        # master_rec_list.append(show_rec)
        # print(show_map[index])
        # print(master_dict_n[escape_db_string(show_map[index])])
        show_name = escape_db_string(show_map[index])
        if show_name in master_dict_n:
            master_rec_dict[master_dict_n[show_name]] = show_rec
        # tl_rec_dict[show_map[index]] = show_rec_tl


        # print('Recommendation for show: ' + show_map[index])
        #
        # print(show_rec)
        # print('Corr scores:', max_a_cos[index])

    # print(master_rec_dict)
    # print(tl_rec_dict)
    if verbose:
        print('Done packing recommendations. Returning to write method.\n')

    return master_rec_dict


def calculate_basic_statistics(c_x, max_users, max_shows, master_dict_n, master_map, show_dict, show_map, user_rating_table_list, verbose=False):
    # print(master_stat_dict)
    master_stat_dict = OrderedDict()

    if verbose:
        print('Loading user rating tables and building histogram...')
    for user_rating_table in user_rating_table_list:
        # print('Reading ratings for: ', user_rating_table)
        c_x.execute('SELECT show, rating FROM [{urt}]'.format(urt=user_rating_table))

        for show_code, rating in c_x.fetchall():
            if show_code in master_map and unescape_db_string(master_map[show_code]) in show_dict:
                if show_code not in master_stat_dict:
                    master_stat_dict[show_code] = {'rating_hist': np.zeros(11), 'var': -1, 'mean': -1, 'std': -1}
                master_stat_dict[show_code]['rating_hist'][rating] += 1

    # print(master_stat_dict[master_dict_n['Sword Art Online']]['rating_hist'])
    # print(master_stat_dict[master_dict_n['Rokka no Yuusha']]['rating_hist'])

    if verbose:
        print('Done generating histogram.')
        print('Calculating mean, variance and standard deviation...')

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

    if verbose:
        print('Done calculations. Returning to write method.\n')

    return master_stat_dict

# max_users = 10000
# max_shows = 500
#
# write_extended_stats(max_users, max_shows, basic_statistics=True, item_rec=True, verbose=True)