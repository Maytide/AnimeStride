import os.path
import sqlite3

import numpy as np

from .RC.RecommenderC import recommend as recommend_c
from .RD.RecommenderD import recommend as recommend_d
from .CreateDFFromDB import create_ratings_dataframe, create_ratings_matrix


class Recommender():
    def __init__(self):
        user_list_db = os.path.dirname(__file__) + '/../data/sample_user_list.db'
        show_list_db = os.path.dirname(__file__) + '/../data/show_data.db'
        conn_u = sqlite3.connect(user_list_db)
        conn_a = sqlite3.connect(show_list_db)
        self.c_u = conn_u.cursor()
        self.c_a = conn_a.cursor()

    def create_user_rating_vector(self, user_ratings, num_shows, shows, verbose=False):
        num_ratings = 0
        user_ratings_vector = np.zeros(num_shows)
        # for i in range(50,100):
        #     my_ratings[i] = (i+3) % 10 + 1
        # print(show_map[i+3])

        for show, rating in user_ratings.items():
            # print(show, rating)
            try:
                user_ratings_vector[shows[show]] = rating
                if int(rating) > 0:
                    num_ratings = num_ratings + 1
            except KeyError as ke:
                if verbose:
                    print('Show ' + str(ke) + ' not in anime db.')
            except TypeError:
                if verbose:
                    print('Type error in building user shows.')

        return num_ratings, user_ratings_vector

    def get_recommendation_c(self, user_ratings, verbose = False, num_recommendations=5, max_users=100, method='generic'):
        num_shows, num_users, ratings_matrix, shows, users = create_ratings_matrix(self.c_u, self.c_a, verbose = verbose, max_users = max_users)
        self.recommendation_c = recommend_c(user_ratings, num_shows, ratings_matrix, shows, users, verbose = verbose, num_recommendations = num_recommendations)
        return self.recommendation_c

    def get_recommendation_d(self, user_ratings, verbose = False, num_recommendations=5, max_users=100, max_shows=500, method='generic'):
        num_shows, num_users, ratings_matrix, shows, users = create_ratings_matrix(self.c_u, self.c_a, verbose=verbose,
                                                                        max_users=max_users, max_shows=max_shows, method=method)
        num_ratings, user_rating_vector = self.create_user_rating_vector(user_ratings, num_shows, shows, verbose=verbose)


        if verbose:
            print('Number of shows: {}'.format(num_shows))
            print('Number of users: {}'.format(num_users))


        self.recommendation_d = recommend_d(user_rating_vector, num_shows, num_users, ratings_matrix, shows, users, verbose=verbose,
                                            num_recommendations=num_recommendations)
        return self.recommendation_d

# user_ratings = {'07-Ghost':10, 'Accel World':10, 'Ajin':10, 'Aldnoah.Zero':10, 'Clannad':1, 'Clannad: After Story':1, 'Fate/stay night Movie: Unlimited Blade Works':10,
#                 'Golden Time':1, 'Hachimitsu to Clover':1, 'Hanasaku Iroha':1, 'Mononoke Hime':1}
#
#
# rec = Recommender()
# rec.get_recommendation_c(user_ratings)
# print(rec.recommendation)
