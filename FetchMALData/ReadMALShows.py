import sqlite3
import urllib.request as urllib
import sys, os
import os.path
import traceback

from Anime import Anime
from FetchMALData.GetAnimePage import AnimePageGetter
from data.open_db import open_db

show_individual_db = os.path.dirname(__file__) + '/../data/show_data_individual.db'
show_aggregated_db = os.path.dirname(__file__) + '/../data/show_data_aggregated.db'
show_indices_db = os.path.dirname(__file__) + '/../data/show_indices.db'

# FMA = Anime('https://myanimelist.net/anime/121/Fullmetal_Alchemist')
# print(FMA.data)

# sj = Anime('https://myanimelist.net/anime/1033/Sennen_Joyuu')
# print(sj.data)


def read_MAL_pages(file_or_db = 'db', write_individual_entry = True, write_aggregated_entry = True, start_page = 0, start_point = 0, end_page = 40, verbose = False, test_mode = False):
    showcount = 0
    flag = False

    item_dict = open_db(0, 10000, open_show_indices=True, open_show_data_aggregated=False, open_user_list_indexed=False, get_conn_n=True, get_conn_x=False)

    for index in range(end_page)[start_page:]:

        # response = ''
        try:
            if index > 0:
                response = urllib.urlopen('https://myanimelist.net/topanime.php?type=bypopularity&limit=' + str(50*(index)))
            elif index == 0:
                response = urllib.urlopen('https://myanimelist.net/topanime.php?type=bypopularity')
        except Exception as ex:
            print('Error in function read_MAL_pages in module ReadMALShows: ' + str(ex))
            print('Could not open top anime page')
            return

        html = str(response.read())

        gap = AnimePageGetter()
        gap.feed(html)

        for anime_URL in gap.data:

            if showcount >= start_point:
                try:
                    anime = Anime()
                    anime.build_data_from_web(anime_URL)
                    content_data_name = anime.content_data['Name:']
                    # print(anime.data)
                    if file_or_db == 'file':
                        anime.write_to_file()
                    elif file_or_db == 'db':
                        # Same db for individual and aggregated - for now.
                        anime.write_to_db(anime_URL, item_dict, show_individual_db, show_aggregated_db, write_individual_entry, write_aggregated_entry)

                    if verbose:
                        # try:
                        #     print(str(showcount) + ' : ' + anime.content_data['Name:'])
                        # except UnicodeEncodeError:
                        #     content_data_name = anime.content_data['Name:'].encode('utf-8')
                        #     sys.stdout.buffer.write(content_data_name)
                        print(str(showcount) + ': ')

                        sys.stdout.buffer.write(content_data_name.encode('utf-8'))
                        print()
                except Exception as ex:
                    print('Error in function read_MAL_pages in module ReadMALShows: ' + str(ex))
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print('Traceback: ')
                    traceback.print_exc()
            showcount = showcount + 1
            if test_mode:
                flag = True


        if flag:
            break
    item_dict['conn_n'].close()


# read_MAL_pages(write_individual_entry = True, write_aggregated_entry = False, start_page = 8, start_point = 6, end_page = 40, verbose = True)
# response = urllib.urlopen('https://myanimelist.net/topanime.php?type=tv')
# html = str(response.read())
#
# gap = AnimePageGetter()
# gap.feed(html)
#
# for anime_URL in gap.data:
#     try:
#         anime = Anime(anime_URL)
#         print(anime.data)
#         anime.write_to_file()
#     except Exception:
#         print(Exception)