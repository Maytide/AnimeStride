## Based off of python implementation of Coursera ML 1 Course.
## https://github.com/mstampfer/Coursera-Stanford-ML-Python
#
from matplotlib import use, cm

use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from scipy.optimize import minimize
# from show import show

## =============== Part 1: Loading movie ratings dataset ================
#  You will start by loading the movie ratings dataset to understand the
#  structure of the data.
#
from cofiCostFunc import cofiCostFunc
from checkCostFunction import checkCostFunction
# from loadMovieList import loadMovieList
from normalizeRatings import normalizeRatings
import CreateDFFromDB as cdf

num_users = 100
ratings_matrix, show_map, user_map = cdf.create_ratings_matrix(user_list_db ='sample_user_list.db',
                                                               show_list_db = 'show_data.db', verbose = True, max_users = num_users)
num_shows = 2000
# Notes: X - num_movies  x num_features matrix of movie features
#        Theta - num_users  x num_features matrix of user features
#        ratings_matrix - num_movies x num_users matrix of user ratings of movies
#        user_rated - num_movies x num_users matrix, where R[i, j] = 1 if the
#        i-th movie was rated by the j-th user

# print(ratings_matrix)
# print(user_rated)
# print(show_map)
my_ratings = np.zeros(num_shows)
for i in range(50,100):
    my_ratings[i] = (i+3) % 10 + 1
    print(show_map[i+3])

ratings_matrix = np.column_stack((my_ratings, ratings_matrix))
R = np.greater(ratings_matrix, np.zeros(ratings_matrix.shape))
# print(user_rated)
# print(ratings_matrix.shape)
ratings_norm, ratings_mean = normalizeRatings(ratings_matrix, R)
# print(ratings_norm)
# print(ratings_mean)
num_users = ratings_matrix.shape[1]
# for row in ratings_matrix:
#     print(row)
# for row in R:
#     print(row)
num_features = 10

X = np.random.rand(num_shows, num_features)
Theta = np.random.rand(num_users, num_features)

initial_parameters = np.hstack((X.T.flatten(), Theta.T.flatten()))
# Set Regularization
Lambda = 10

print(num_users, num_shows, num_features)
costFunc = lambda p: cofiCostFunc(p, ratings_norm, R, num_users, num_shows, num_features, Lambda)[0]
gradFunc = lambda p: cofiCostFunc(p, ratings_norm, R, num_users, num_shows, num_features, Lambda)[1]

result = minimize(costFunc, initial_parameters, method='CG', jac=gradFunc, options={'disp': True, 'maxiter': 50.0})
theta = result.x
cost = result.fun

X = theta[:num_shows * num_features].reshape(num_shows, num_features)
Theta = theta[num_shows * num_features:].reshape(num_users, num_features)

print('Recommender system learning completed.')

input("Program paused. Press Enter to continue...")

p = X.dot(Theta.T)
my_predictions = p[:, 0] + ratings_mean

pre=np.array([[idx, p] for idx, p in enumerate(my_predictions)])
post = pre[pre[:,1].argsort()[::-1]]
r = post[:,1]
ix = post[:,0]

print('\nTop recommendations for you:')

for i in range(50):
    j = int(ix[i])
    print('Predicting rating %.1f for show %s\n' % (my_predictions[j], show_map[j]))

# print('\nOriginal ratings provided:')
# for i in range(len(my_ratings)):
#     if my_ratings[i] > 0:
#         print('Rated %d for %s\n' % (my_ratings[i], show_map[i]))
# movieList = loadMovieList()
#
# # sort predictions descending
# pre = np.array([[idx, p] for idx, p in enumerate(my_predictions)])
# post = pre[pre[:, 1].argsort()[::-1]]
# r = post[:, 1]
# ix = post[:, 0]
#
# print('\nTop recommendations for you:')
#
# for i in range(10):
#     j = int(ix[i])
#     print('Predicting rating %.1f for movie %s\n' % (my_predictions[j], movieList[j]))
#
# print('\nOriginal ratings provided:')
# for i in range(len(my_ratings)):
#     if my_ratings[i] > 0:
#         print('Rated %d for %s\n' % (my_ratings[i], movieList[i]))
