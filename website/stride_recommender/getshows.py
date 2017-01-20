from random import randint

from .models import ContentData


def get_shows_random(num_shows=3):
    shows = [ContentData.objects.all()[randint(0, 1999)] for i in range(num_shows)]
    return shows

def get_shows_url(url, num_shows=3):
    shows = [ContentData.objects.all()[len(url)] for i in range(num_shows)]
    return shows