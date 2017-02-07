import math

from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
from scipy.spatial.distance import cosine

import numpy as np


def pearson_correlation(user, train_matrix, verbose=False):
    max_corr = -1
    min_corr = 1
    corr_vector = []
    for index, row in enumerate(train_matrix):
        num_nonzero = 0
        user_nonzero = []
        row_nonzero = []
        for user_score, row_score in zip(user, row):
            # 'Mutuality' regularization:
            # The more shows in common, the higher in confidence the r value.
            #
            if user_score > 0 and row_score > 0:
                user_nonzero.append(user_score)
                row_nonzero.append(row_score)
                num_nonzero = num_nonzero + 1

        if len(user) >= 40 and len(user_nonzero) <= 20:
            continue
        elif len(user) >= 20 and len(user_nonzero) <= 5:
            continue

        # print(user)
        # print(row)
        # Handle case of NaN
        if np.sum(row_nonzero) == 0:
            continue
        r, p = pearsonr(user_nonzero, row_nonzero)
        # WAnt to map from sample rating -> user rating
        # So do np.polyfit row_nonzero, user_nonzero
        l = np.polyfit(row_nonzero, user_nonzero, 1)
        lobf = {'y-int' : l[1], 'slope' : l[0]}
        if not math.isnan(r):
            corr_vector.append([index, len(user_nonzero), r, lobf])
        if r > max_corr:
            max_corr = r
        if r < min_corr:
            min_corr = r

    # print('User has rated ' + str(np.count_nonzero(user)) + ' shows.')
    if verbose:
        print('Max correlation: ' + str(max_corr))
        print('Min correlation: ' + str(min_corr))

    corr_vector.sort(key=lambda p: p[2], reverse=True)
    if verbose:
        print('Correlation Vector:')
        print(corr_vector)
    return corr_vector

def recommend(user_ratings_vector, num_shows, num_users, ratings_matrix, shows, users, verbose = False, num_recommendations = 5):
    show_map = {index: show for show, index in shows.items()}
    user_map = {index: user for user, index in users.items()}

    corr_vector = pearson_correlation(user_ratings_vector, ratings_matrix)
    mean_ratings = np.zeros(num_shows)
    mean_ratings_count = np.zeros(num_shows)

    for i in range(len(ratings_matrix)):
        for j in range(num_shows):
            if ratings_matrix[i][j] > 0:
                mean_ratings[j] = mean_ratings[j] + ratings_matrix[i][j]
                mean_ratings_count[j] = mean_ratings_count[j] + 1

    for num_ratings in np.nditer(mean_ratings_count, op_flags=['readwrite']):
        if num_ratings == 0:
            # MUST use += syntax!
            # http://stackoverflow.com/a/34652053
            num_ratings += 1
    mean_ratings = np.divide(mean_ratings, mean_ratings_count)

    # Helper functions that calculate errors
    #########################
    def sum_nonzero(accumulator, new_entry, nonzero_count, vector_len, index):

        score_map = lambda p: corr_vector[index][3]['y-int'] + corr_vector[index][3]['slope'] * p

        for i in range(vector_len):
            if new_entry[i] > 0:
                accumulator[i] = accumulator[i] + score_map(new_entry[i])
                nonzero_count[i] = nonzero_count[i] + 1

        return accumulator, nonzero_count

    def RMSE_nonzero(v1, v2, vector_len, return_count=False):
        sum = 0
        count = 0
        for i in range(vector_len):
            if v1[i] > 0 and v2[i] > 0:
                sum = sum + (v1[i] - v2[i])**2
                count = count + 1

        if count > 0:
            sum = math.sqrt(sum/count)
        else:
            sum = 0

        if return_count:
            return sum, count
        else:
            return sum

    def AE_nonzero(v1, v2, vector_len, return_count=False):
        sum = 0
        count = 0
        for i in range(vector_len):
            if v1[i] > 0 and v2[i] > 0:
                sum = sum + abs(v1[i] - v2[i])
                count = count + 1

        if count > 0:
            sum = sum/count
        else:
            sum = 0

        if return_count:
            return sum, count
        else:
            return sum

    #########################

    corr_sample_size = 16

    # Recommender
    #########################

    def recommend_corr():
        user_corr_weighted = np.zeros(num_shows)
        user_corr_unweighted = np.zeros(num_shows)
        user_corr_unweighted_R = np.zeros(num_shows)

        # corr_vector: Vector of form (user_index, number of shows in common, pearson correlation, LOBF array: (slope, y-int) )
        # IMPORTANT: LOBF array maps from sample_ratings to user_ratings!
        corr_sum = 0
        for index in range(corr_sample_size):
            sample_ratings = ratings_matrix[corr_vector[index][0]]
            sample_corr = corr_vector[index][2]
            corr_sum = corr_sum + sample_corr

            # y = mx + b for every rating in the sample matrix to map it to an
            # equivalent score in the user matrix


            # user_corr_unweighted = user_corr_unweighted + score_map(sample_ratings)
            # print(user_corr_unweighted_R)
            user_corr_unweighted, user_corr_unweighted_R = sum_nonzero(user_corr_unweighted, sample_ratings, user_corr_unweighted_R, num_shows, index)

            pass

        for num_ratings in np.nditer(user_corr_unweighted_R, op_flags=['readwrite']):
            if num_ratings == 0:
                # MUST use += syntax!
                # http://stackoverflow.com/a/34652053
                num_ratings += 1

        # print(user_corr_unweighted_R)
        user_corr_unweighted = np.divide(user_corr_unweighted, user_corr_unweighted_R)
        # print(user_corr_unweighted)
        control_average = 0
        user_count = 0
        user_watched = []
        user_not_watched = []
        for i in range(num_shows):
            if user_ratings_vector[i] > 0:
                control_average = control_average + user_ratings_vector[i]
                user_count = user_count + 1
                user_watched.append([show_map[i], i, user_corr_unweighted[i]])
            else:
                user_not_watched.append([show_map[i], i, user_corr_unweighted[i]])
            # if user_corr_unweighted[i] > 0 and user_show_list[i] > 0:
            #     print('Show: ' + show_map[i])
            #     print(user_corr_unweighted[i], user_show_list[i])
            #     print()

        control_average = control_average / user_count

        control_vector = np.zeros(num_shows)
        control_vector = control_vector + control_average

        rmse, count = RMSE_nonzero(user_corr_unweighted, user_ratings_vector, num_shows, return_count=True)
        ae = AE_nonzero(user_corr_unweighted, user_ratings_vector, num_shows, return_count=False)
        control_rmse = RMSE_nonzero(control_vector, user_ratings_vector, num_shows, return_count=True)
        control_ae = AE_nonzero(control_vector, user_ratings_vector, num_shows, return_count=True)

        if verbose:
            print('RMSE: ' + str(rmse) + ', AE: ' + str(ae) + ', Count:' + str(count))
            print('Control RMSE: ' + str(control_rmse) + ', Control AE: ' + str(control_ae) + ', Count:' + str(count))

        # if show_hist:
        #     plt.hist(user_watched)
        #     plt.show()

        user_not_watched.sort(key=lambda p:p[2], reverse=True)
        # print(mean_ratings)
        # if verbose:
        #     print(user_watched)
        #     print(user_not_watched)

        max_diff_unwatched = list()

        for i in range(len(user_not_watched)):
            # Predicted user rating - overall mean rating of all users
            if user_not_watched[i][2] > 7 and mean_ratings[user_not_watched[i][1]] > 6.5:
                diff = user_not_watched[i][2] - mean_ratings[user_not_watched[i][1]]
                max_diff_unwatched.append([user_not_watched[i][0], diff, user_not_watched[i][2], mean_ratings[user_not_watched[i][1]]])

        max_diff_watched = list()

        for i in range(len(user_watched)):
            # Predicted user rating - overall mean rating of all users
            if user_watched[i][2] > 7 and mean_ratings[user_watched[i][1]] > 6.5:
                diff = user_watched[i][2] - mean_ratings[user_watched[i][1]]
                max_diff_watched.append([user_watched[i][0], diff, user_watched[i][2], mean_ratings[user_watched[i][1]]])

        max_diff_unwatched.sort(key=lambda p: p[1], reverse=True)
        max_diff_watched.sort(key=lambda p: p[1], reverse=True)
        if verbose:
            print('max_diff_unwatched')
            print(max_diff_unwatched)
            print('max_diff_watched')
            print(max_diff_watched)


        user_not_watched = user_not_watched[:5]
        max_diff_unwatched = max_diff_unwatched[:5]
        recommend_flavors = {'top-rated': user_not_watched, 'top-diff': max_diff_unwatched, 'rmse-generic-prediction': rmse, 'ae-generic-prediction': ae}


        return recommend_flavors

    recommend_flavors = recommend_corr()

    #########################

    # print('User has rated ' + str(np.count_nonzero(user_show_list)) + ' shows.')
    return recommend_flavors
    pass