from .RC.RecommenderC import recommend as recommend_c
from .CreateDFFromDB import create_ratings_dataframe, create_ratings_matrix
import os.path
import sqlite3


class Recommender():
    def __init__(self):
        user_list_db = os.path.dirname(__file__) + '/../data/sample_user_list.db'
        show_list_db = os.path.dirname(__file__) + '/../data/show_data.db'
        conn_u = sqlite3.connect(user_list_db)
        conn_a = sqlite3.connect(show_list_db)
        self.c_u = conn_u.cursor()
        self.c_a = conn_a.cursor()

    def get_recommendation_c(self, user_ratings, verbose = False):
        num_shows, ratings_matrix, shows, users = create_ratings_matrix(self.c_u, self.c_a, verbose = verbose, max_users = 100)
        self.recommendation_c = recommend_c(user_ratings, num_shows, ratings_matrix, shows, users, verbose = verbose)
        return self.recommendation_c

# user_ratings = {'07-Ghost':10, 'Accel World':10, 'Ajin':10, 'Aldnoah.Zero':10, 'Clannad':1, 'Clannad: After Story':1, 'Fate/stay night Movie: Unlimited Blade Works':10,
#                 'Golden Time':1, 'Hachimitsu to Clover':1, 'Hanasaku Iroha':1, 'Mononoke Hime':1}
#
#
# rec = Recommender()
# rec.get_recommendation_c(user_ratings)
# print(rec.recommendation)
