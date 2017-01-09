import numpy as np
import pandas as pd
from sklearn import cross_validation as cv
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import mean_squared_error
import scipy.sparse as sp
from scipy.sparse.linalg import svds
from math import sqrt
import CreateDFFromDB as cdf


# Collaborative Filtering code from:
# http://online.cambridgecoding.com/notebooks/eWReNYcAfB/implementing-your-own-recommender-systems-in-python-2
# Fix for large error in comments

def rmse(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    # for index, item in enumerate(prediction):
    #     print('Prediction: ' + str(prediction[index]))
    #     print('Actual: ' + str(ground_truth[index]))
    return sqrt(mean_squared_error(prediction, ground_truth))

def ae(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()

    return abs(prediction - ground_truth).sum()/len(prediction)

def predict(ratings, similarity, type='user'):
    mask = np.copy(ratings)
    mask[ratings > 0] = 1
    # print(ratings)
    # Mask: n_users x n_shows matrix
    # print(type + ': ' + str(len(mask)))
    # print(type + ': ' + str(len(mask[0])))



    if type == 'user':
        sum = np.sum(ratings, axis=1)
        nonzero_rating = []
        for index, rating in enumerate(ratings):
            nonzero_rating.append(np.count_nonzero(ratings[index]))
            # print(nonzero_rating[index])
        nonzero_rating = [1 if rating == 0 else rating for rating in nonzero_rating]

        mean_user_rating = np.divide(sum, nonzero_rating)
        row_sums = similarity.sum(axis=1)
        similarity_norm = 3 * similarity / row_sums[:, np.newaxis]
        # mean_user_rating = ratings.mean(axis=1)
        # print(mean_user_rating[:, np.newaxis])
        # print(similarity_norm)
        # You use np.newaxis so that mean_user_rating has same format as ratings
        ratings_diff = np.multiply(ratings - mean_user_rating[:, np.newaxis], mask)
        # print(ratings_diff)
        # print('diff ' + str(len(ratings_diff)))
        # print('diff ' + str(len(ratings_diff[0])))
        # print('rate ' + str(len(ratings)))
        # print('rate ' + str(len(ratings[0])))
        # print('mean ' + str(len(mean_user_rating[:, np.newaxis])))
        # print('mean ' + str(len(mean_user_rating[:, np.newaxis][0])))
        # ratings_diff = (ratings - np.multiply(mean_user_rating[:, np.newaxis], mask))
        # pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
        pred = mean_user_rating[:, np.newaxis] + similarity_norm.dot(ratings_diff)
        # pred = []
        # print(pred)
        # print('Mean user rating: ' + str(len(mean_user_rating[:, np.newaxis])))
        # print('Mean user rating: ' + str(len(mean_user_rating[:, np.newaxis][0])))
        # print('Similarity: ' + str(len(similarity)))
        # print('Similarity: ' + str(len(similarity[0])))
        # print('Similarity dot ratings diff: ' + str(len(similarity.dot(ratings_diff))))
        # print('Similarity dot ratings diff: ' + str(len(similarity.dot(ratings_diff)[0])))
        # print('Denominator: ' + str(len(np.array([np.abs(similarity).sum(axis=1)]).T)))
        # print('Denominator: ' + str(len(np.array([np.abs(similarity).sum(axis=1)]).T[0])))
        # print('fraction: ' + str(len(similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T)))
        # print('fraction: ' + str(len(similarity.dot((ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T)[0])))
        # print('predict: ' + str(len(pred)))
        # print('predict: ' + str(len(pred[0])))
        # pred = np.multiply(pred, mask)
    elif type == 'item':
        pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    return pred



(ratings_dataframe, show_map, user_map) = cdf.create_ratings_dataframe(user_list_db ='sample_user_list.db', show_list_db = 'show_data.db',
                                                                       max_users = 500, verbose = True)
# print(ratings_dataframe)
# print(show_map)
# print(user_map)

n_users = ratings_dataframe.user.unique().shape[0]
n_shows = ratings_dataframe.anime.unique().shape[0]
print('Number of users = ' + str(n_users) + ' | Number of shows = ' + str(n_shows))

train_data, test_data = cv.train_test_split(ratings_dataframe, test_size=0.25)

#Create two user-item matrices, one for training and another for testing
train_data_matrix = np.zeros((n_users, n_shows))
for line in train_data.itertuples():
    # print('1: ' + line[1])
    # print('2: ' + line[2])
    # print('3: ' + line[3])
    train_data_matrix[line[1]-1, line[2]-1] = line[3]

test_data_matrix = np.zeros((n_users, n_shows))
for line in test_data.itertuples():
    test_data_matrix[line[1]-1, line[2]-1] = line[3]

user_similarity = pairwise_distances(train_data_matrix, metric='manhattan')
show_similarity = pairwise_distances(train_data_matrix.T, metric='manhattan')

item_prediction = predict(train_data_matrix, show_similarity, type='item')
user_prediction = predict(train_data_matrix, user_similarity, type='user')

# print(train_data_matrix)
# print('User predictiona: ' + str(len(user_prediction)))
# for item in user_prediction:
#     print('Item in user prediction: ' + str(item))
#     rating = np.rint(item)
#     hist = np.histogram(rating)
#     print(hist)
#     print('newline \n')


u, s, vt = svds(train_data_matrix, k = 20)
s_diag_matrix=np.diag(s)
X_pred = np.dot(np.dot(u, s_diag_matrix), vt)


print('User-based CF RMSE: ' + str(rmse(user_prediction, test_data_matrix)))
print('User-based CF AE: ' + str(ae(user_prediction, test_data_matrix)))
# print('Item-based CF RMSE: ' + str(rmse(item_prediction, test_data_matrix)))
# print('User-based CF MSE: ' + str(rmse(X_pred, test_data_matrix)))
# print('User-based CF AE: ' + str(ae(X_pred, test_data_matrix)))
# First 100 users
# Manhattan:
# User-based CF RMSE: 6.07177500808337
# Item-based CF RMSE: 6.530507485927438
# User-based CF MSE: 6.09591402272522
#
# Cosine:
# User-based CF RMSE: 6.185248122497281
# Item-based CF RMSE: 6.881971552017517
# User-based CF MSE: 6.15971535757973
#
# Euclidean:
# User-based CF RMSE: 6.14061442959285
# Item-based CF RMSE: 6.722791347900957
# User-based CF MSE: 6.14940153276465