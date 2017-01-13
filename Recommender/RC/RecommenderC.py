## Based off of python implementation of Coursera ML 1 Course.
## https://github.com/mstampfer/Coursera-Stanford-ML-Python
##

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
from .cofiCostFunc import cofiCostFunc
# from loadMovieList import loadMovieList
from .normalizeRatings import normalizeRatings

def recommend(user_ratings, num_shows, ratings_matrix, shows, users, verbose = False, num_users = 100, num_recommendations = 5):

    # num_users = 100
    # num_shows, ratings_matrix, shows, users = cdf.create_ratings_matrix(user_list_db = user_list_db,
    #                                                                     show_list_db = show_list_db, verbose = verbose, max_users = num_users)

    # Notes: X - num_movies  x num_features matrix of movie features
    #        Theta - num_users  x num_features matrix of user features
    #        ratings_matrix - num_movies x num_users matrix of user ratings of movies
    #        user_rated - num_movies x num_users matrix, where R[i, j] = 1 if the
    #        i-th movie was rated by the j-th user

    # user_ratings: dict of 'show_name' : rating
    show_map = {index: show for show, index in shows.items()}
    user_map = {index: user for user, index in users.items()}
    # print(ratings_matrix)
    # print(user_rated)
    # print(show_map)
    my_ratings = np.zeros(num_shows)
    # for i in range(50,100):
    #     my_ratings[i] = (i+3) % 10 + 1
        # print(show_map[i+3])
    for show, rating in user_ratings.items():
        try:
            my_ratings[shows[show]] = rating
        except KeyError as ke:
            if verbose:
                print('Show ' + str(ke) + ' not in anime db.')

    ratings_matrix_ = np.column_stack((my_ratings, ratings_matrix))
    R = np.greater(ratings_matrix_, np.zeros(ratings_matrix_.shape))
    # print(user_rated)
    # print(ratings_matrix.shape)
    ratings_norm, ratings_mean = normalizeRatings(ratings_matrix_, R)
    # print(ratings_norm)
    # print(ratings_mean)
    num_users = ratings_matrix_.shape[1]
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

    if verbose:
        print(num_users, num_shows, num_features)

    costFunc = lambda p: cofiCostFunc(p, ratings_norm, R, num_users, num_shows, num_features, Lambda)[0]
    gradFunc = lambda p: cofiCostFunc(p, ratings_norm, R, num_users, num_shows, num_features, Lambda)[1]

    result = minimize(costFunc, initial_parameters, method='CG', jac=gradFunc, options={'disp': verbose, 'maxiter': 50.0})
    theta = result.x
    cost = result.fun

    X = theta[:num_shows * num_features].reshape(num_shows, num_features)
    Theta = theta[num_shows * num_features:].reshape(num_users, num_features)

    if verbose:
        print('Recommender system learning completed.')

    # input("Program paused. Press Enter to continue...")

    p = X.dot(Theta.T)
    my_predictions = p[:, 0] + ratings_mean

    pre=np.array([[idx, p] for idx, p in enumerate(my_predictions)])
    post = pre[pre[:,1].argsort()[::-1]]
    r = post[:,1]
    ix = post[:,0]

    prediction = []
    # print('\nTop recommendations for you:')
    #
    for i in range(num_recommendations):
        j = int(ix[i])
        prediction.append([my_predictions[j], show_map[j]])
        # print('Predicting rating %.1f for show %s\n' % (my_predictions[j], show_map[j]))


    return prediction
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
