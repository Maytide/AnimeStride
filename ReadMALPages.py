from Anime import Anime
from GetAnimePage import AnimePageGetter
import urllib.request as urllib


# FMA = Anime('https://myanimelist.net/anime/121/Fullmetal_Alchemist')

response = urllib.urlopen('https://myanimelist.net/topanime.php?type=tv')
html = str(response.read())

gap = AnimePageGetter()
gap.feed(html)

print(gap.data)