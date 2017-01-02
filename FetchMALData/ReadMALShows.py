from FetchMALData.Anime import Anime
from FetchMALData.GetAnimePage import AnimePageGetter
import urllib.request as urllib
import sqlite3


# FMA = Anime('https://myanimelist.net/anime/121/Fullmetal_Alchemist')
# print(FMA.data)

# sj = Anime('https://myanimelist.net/anime/1033/Sennen_Joyuu')
# print(sj.data)


def read_MAL_pages(file_or_db = 'db', write_individual_entry = True, write_aggregated_entry = True):
    showcount = 0
    for index in range(40)[20:]:
        # response = ''
        if index > 0:
            response = urllib.urlopen('https://myanimelist.net/topanime.php?type=bypopularity&limit=' + str(50*(index)))
        elif index == 0:
            response = urllib.urlopen('https://myanimelist.net/topanime.php?type=bypopularity')

        html = str(response.read())

        gap = AnimePageGetter()
        gap.feed(html)

        for anime_URL in gap.data:
            try:
                anime = Anime(anime_URL)
                # print(anime.data)
                if file_or_db == 'file':
                    anime.write_to_file()
                elif file_or_db == 'db':
                    # Same db for individual and aggregated - for now.
                    anime.write_to_db('show_data.db', 'show_data.db', write_individual_entry, write_aggregated_entry)
                print(str(showcount) + ' : ' + anime.content_data['Name:'])
            except Exception as ex:
                print('Error in function read_MAL_pages in module ReadMALShows: ' + str(ex))
            showcount = showcount + 1

# Should never have to call this function again, ever. (After parsing in User class fixed to remove outer quotes)
def remove_outer_quotes(db = 'sample_user_list.db'):
    # Prone to injection
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute('''SELECT name FROM sqlite_master WHERE type="table";''')
    tables_list = ['[' + item[0] + ']' for item in c.fetchall()]
    # tables_list = c.fetchall()

    for i, table in enumerate(tables_list):
        # print(type(table))
        print('index: ' + str(i) + ', table: ' + table)
        c.execute('''SELECT "anime" FROM {}'''.format(table))
        row_list = [item[0] for item in c.fetchall()]
        # print(row_list)
        # table = table[:-1] if table.endswith(']') else table
        # table = table[1:] if table.startswith('[') else table
        # print(table)
        for index, row in enumerate(row_list):
            # print(row)
            row_list[index] = row[:-1] if row.endswith('"') else row
            row_list[index] = row_list[index][1:] if row.startswith('"') else row
            # print(row_list[index])
            # http://stackoverflow.com/questions/25387537/sqlite3-operationalerror-near-syntax-error
            # Use String.format for database object;
            # Use sql parameter formatting for non-database objects
            c.execute('''UPDATE {} SET "anime" = ? WHERE "anime" = ?'''.format(table), (row_list[index], row))
            # print(row)
        # print(table)
        c.execute('''SELECT "anime" from {}'''.format(table))
        # print(len(c.fetchall()))

        #
        #     print(row)
        #     c.execute('''SELECT "anime" from {}'''.format(row))

        # c.execute('''UPDATE {} '''.format(table))
    conn.commit()
    conn.close()
remove_outer_quotes()
# read_MAL_pages()
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