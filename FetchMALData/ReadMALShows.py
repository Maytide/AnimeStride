from FetchMALData.Anime import Anime
from FetchMALData.GetAnimePage import AnimePageGetter
import urllib.request as urllib


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

read_MAL_pages()
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