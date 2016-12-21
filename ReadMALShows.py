from Anime import Anime
from GetAnimePage import AnimePageGetter
import urllib.request as urllib


# FMA = Anime('https://myanimelist.net/anime/121/Fullmetal_Alchemist')
# print(FMA.data)



# sj = Anime('https://myanimelist.net/anime/1033/Sennen_Joyuu')
# print(sj.data)


def read_MAL_pages():

    for index in range(20):
        response = urllib.urlopen('https://myanimelist.net/topanime.php?type=bypopularity')
        if index > 0:
            response = urllib.urlopen('https://myanimelist.net/topanime.php?type=bypopularity&limit=' + str(50*(index)))
        html = str(response.read())

        gap = AnimePageGetter()
        gap.feed(html)

        for anime_URL in gap.data:
            try:
                anime = Anime(anime_URL)
                print(anime.data)
                anime.write_to_file()
            except Exception as ex:
                print(ex)

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