import sys
from random import randint

from django.conf import settings
sys.path.append(settings.PROJECT_ROOT)
from Anime import Anime
from master import string_delimiter_upper, japanese_particles
sys.path.remove(settings.PROJECT_ROOT)

from .models import ContentData, BasicStatistics, ItemRecs


def get_show(show_name):
    show = None
    try:
        show = ContentData.objects.get(pk=show_name)
        return show
    except Exception as ex:
        pass

    try:
        show = ContentData.objects.get(pk=string_delimiter_upper(show_name, ' ', exception_list=japanese_particles))
        return show
    except Exception as ex:
        pass

        pass

    return show


def get_show_basic_stats(show_name):
    show = None
    # print(show_name)
    try:
        show = BasicStatistics.objects.get(pk=show_name)
        return show
    except Exception as ex:

        pass

    try:
        show = BasicStatistics.objects.get(pk=string_delimiter_upper(show_name, ' ', exception_list=japanese_particles))
        return show
    except Exception as ex:
        print('[stride_stats: getshows: basic_stats] Could not process show.', ex)
        pass


    return show

def get_show_item_rec(show_name):
    show = None
    try:
        show = ItemRecs.objects.get(pk=show_name)
        # print(show)
        return show
    except Exception as ex:
        pass

    try:
        show = ItemRecs.objects.get(pk=string_delimiter_upper(show_name, ' ', exception_list=japanese_particles))
        # print(show)
        return show
    except Exception as ex:
        print('[stride_stats: getshows: item rec] Could not process show.', ex)
        pass

    return show

def get_show_stats(show_name, max_recall=30):
    anime = Anime()
    anime.build_stats_from_db(show_name, max_recall)

    stats_dict = anime.full_stats
    timestamp = anime.timestamp

    return stats_dict, timestamp


def get_shows(num_shows=10):
    show_list = [ContentData.objects.all()[i] for i in range(num_shows)]
    return show_list


def get_shows_random(num_shows=9):
    try:
        num_shows_ = int(num_shows)
    except Exception as ex:
        num_shows_ = 9

    show_list = [ContentData.objects.all()[randint(0, 1999)] for i in range(num_shows_)]
    return show_list


def get_shows_popularity(num_shows=50):

    try:
        num_shows_ = int(num_shows)
    except Exception as ex:
        num_shows_ = 50

    show_list = ContentData.objects.order_by('popularity')[:num_shows_]
    # print(show_list)

    return show_list


###################################
# Test methods

def get_show_test2(show_name):
    return [len(show_name) % 12, len(show_name) % 19, len(show_name) % 3, len(show_name) % 5, len(show_name) % 6, len(show_name) % 7]

def get_show_test():
    return [12, 19, 3, 5, 2, 3]

