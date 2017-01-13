## Based off of python implementation of Coursera ML 1 Course.
## https://github.com/mstampfer/Coursera-Stanford-ML-Python
##

import numpy as np


def cofiCostFunc(params, Y, R, num_users, num_shows, num_features, Lambda):
    """returns the cost and gradient for the
    """

    # Unfold the U and W matrices from params
    X = np.array(params[:num_shows * num_features]).reshape(num_features, num_shows).T.copy()
    Theta = np.array(params[num_shows * num_features:]).reshape(num_features, num_users).T.copy()


    # You need to return the following values correctly
    J = 0
    X_grad = np.zeros(X.shape)
    Theta_grad = np.zeros(Theta.shape)

    # ====================== YOUR CODE HERE ======================
    # Instructions: Compute the cost function and gradient for collaborative
    #               filtering. Concretely, you should first implement the cost
    #               function (without regularization) and make sure it is
    #               matches our costs. After that, you should implement the
    #               gradient and use the checkCostFunction routine to check
    #               that the gradient is correct. Finally, you should implement
    #               regularization.
    #
    # Notes: X - num_movies  x num_features matrix of movie features
    #        Theta - num_users  x num_features matrix of user features
    #        Y - num_movies x num_users matrix of user ratings of movies
    #        R - num_movies x num_users matrix, where R(i, j) = 1 if the
    #            i-th movie was rated by the j-th user
    #
    # You should set the following variables correctly:
    #
    #        X_grad - num_movies x num_features matrix, containing the
    #                 partial derivatives w.r.t. to each element of X
    #        Theta_grad - num_users x num_features matrix, containing the
    #                     partial derivatives w.r.t. to each element of Theta

    # Calculate cost function
    t = np.dot(X, Theta.T) - Y
    t2 = np.multiply(t, np.multiply(t, R))

    J = 1/2 * t2.sum(axis=0).sum(axis=0)

    # J = J + Lambda/2 * np.multiply(Theta, Theta).sum(axis=0).sum(axis=0)
    # J = J + Lambda/2 * np.multiply(X, X).sum(axis=0).sum(axis=0)
    # J = J + lambda / 2 * sum(sum(Theta.^ 2));
    # J = J + lambda / 2 * sum(sum(X.^ 2));

    # Calculate X gradient
    # print(num_movies)
    for i in range(num_shows):
        idx = R[i,:] == 1
        # print(idx)
        # print('')
        Theta_rated = Theta[idx,:]
        Y_rated = Y[i,idx]
        X_grad[i,:] = np.dot(np.dot(X[i,:], Theta_rated.T) - Y_rated, Theta_rated) + Lambda*X[i,:]

    # print(X_grad)
    # Calculate theta gradient
    for j in range(num_users):
        idx = R[:, j] == 1


        X_rated = X[idx,:]
        Y_rated = Y[idx,j]
        Theta_grad[j,:] = np.dot((np.dot(X_rated, Theta[j,:].T) - Y_rated).T, X_rated) + Lambda*Theta[j,:]


    # =============================================================

    grad = np.hstack((X_grad.T.flatten(),Theta_grad.T.flatten()))

    return J, grad
