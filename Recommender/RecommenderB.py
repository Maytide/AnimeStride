import pandas as pd
from scipy.spatial.distance import cosine
import CreateDFFromDB as cdf

(ratings_dataframe, show_map, user_map) = cdf.create_ratings_dataframe(user_list_db ='sample_user_list.db', show_list_db = 'show_data.db', max_users = 20, verbose = False)

print(ratings_dataframe.head(n=3))

items_data = ratings_dataframe.drop('user', axis=1)
items_dataframe = pd.DataFrame(index=items_data.columns, columns = items_data.columns)

print(items_dataframe)

for i in range(len(items_dataframe.columns)):
    for j in range(len(items_dataframe.columns)):
        # if type(items_data.ix[:,i]) == type('s'):
        #     print('i: ' + items_data.ix[:,i])
        # if type(items_data.ix[:,j]) == type('s'):
        #     print('j: ' + items_data.ix[:,j])
        # print('i: ' + str(items_data.ix[:, i]))
        # print('j: ' + str(items_data.ix[:, j]))
        items_dataframe[i,j] = 1 - cosine(items_data.ix[:,i], items_data.ix[:,j])

neighbors = pd.DataFrame(index=items_dataframe.columns,columns=range(1,11))

for i in range(0,len(items_dataframe.columns)):
    neighbors.ix[i,:10] = items_dataframe.ix[0:,i].order(ascending=False)[:10].index

print(neighbors.head(n=6))