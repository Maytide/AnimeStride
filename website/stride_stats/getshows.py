import sys
from random import randint
import datetime, time

from django.conf import settings
sys.path.append(settings.PROJECT_ROOT)
from Anime import Anime
from master import string_delimiter_upper, japanese_particles, EMPTY_STATS_DICT, EMPTY_CONTENT_DATA, \
    unescape_url_chars
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
        show = ContentData.objects.get(pk=EMPTY_CONTENT_DATA)
        pass



    return show


def get_show_basic_stats(show_name):
    # print('[stride_stats: getshows: basic_stats] show name:', show_name)
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
        show = get_show_basic_stats(EMPTY_CONTENT_DATA)
        pass


    return show

def get_show_item_rec(show_name):
    show_list = []
    show = None
    try:
        show = ItemRecs.objects.get(pk=show_name)
        # print(show)
    except Exception as ex:
        try:
            show = ItemRecs.objects.get(pk=string_delimiter_upper(show_name, ' ', exception_list=japanese_particles))
            # print(show)
        except Exception as ex:
            print('[stride_stats: getshows: item rec] Could not process show:', show_name, ex)
            return get_shows_random(num_shows=6)

    # print('[stride_stats: getshows: item rec] Show:', show)
    for rec in show.get_recs():
        try:
            show_list.append(ContentData.objects.get(pk=rec))
        except Exception as ex:
            print('[stride_stats: getshows: item rec] Could not process show:', rec, ex)
            pass

    return show_list

def get_show_stats(show_name, max_recall=30):
    anime = Anime()
    anime.build_stats_from_db(show_name, max_recall)

    stats_dict = anime.full_stats
    timestamp = anime.timestamp

    # If show not found in database
    if isinstance(stats_dict, list):
        stats_dict = EMPTY_STATS_DICT['values']
        timestamp = EMPTY_STATS_DICT['axis_labels']

    return stats_dict, timestamp


def get_show_stats_month(show_name, max_recall=30):
    anime = Anime()
    anime.build_stats_from_db(show_name, max_recall)

    stats_dict = anime.full_stats
    timestamp = anime.timestamp

    if isinstance(stats_dict, list):
        stats_dict = EMPTY_STATS_DICT['values']
        timestamp = EMPTY_STATS_DICT['axis_labels']

    return stats_dict, timestamp


def get_show_stats_season(show_name, max_recall=90):
    anime = Anime()
    anime.build_stats_from_db(show_name, max_recall, nth=3)

    # stats_dict, timestamp = [zip(stat, time) for index, (stat, time) in enumerate()]
    stats_dict = anime.full_stats
    timestamp = anime.timestamp

    if isinstance(stats_dict, list):
        stats_dict = EMPTY_STATS_DICT['values']
        timestamp = EMPTY_STATS_DICT['axis_labels']
    # stats_dict = [stat for index, stat in enumerate(anime.full_stats) if index % 3 == 0]
    # timestamp = [time for index, time in enumerate(anime.timestamp) if index % 3 == 0 ]

    # print(stats_dict)
    # print(timestamp)

    return stats_dict, timestamp


def get_show_stats_year(show_name, max_recall=365):
    anime = Anime()
    anime.build_stats_from_db(show_name, max_recall, nth=12)

    # stats_dict, timestamp = [zip(stat, time) for index, (stat, time) in enumerate()]
    stats_dict = anime.full_stats
    timestamp = anime.timestamp

    if isinstance(stats_dict, list):
        stats_dict = EMPTY_STATS_DICT['values']
        timestamp = EMPTY_STATS_DICT['axis_labels']
    # stats_dict = [stat for index, stat in enumerate(anime.full_stats) if index % 30 == 0]
    # timestamp = [time for index, time in enumerate(anime.timestamp) if index % 30 == 0]

    return stats_dict, timestamp


def get_show_stats_all(show_name, max_recall=10000):
    anime = Anime()
    anime.build_stats_from_db(show_name, max_recall, nth=30)

    # stats_dict, timestamp = [zip(stat, time) for index, (stat, time) in enumerate()]
    stats_dict = anime.full_stats
    timestamp = anime.timestamp

    if isinstance(stats_dict, list):
        stats_dict = EMPTY_STATS_DICT['values']
        timestamp = EMPTY_STATS_DICT['axis_labels']
    # stats_dict = [stat for index, stat in enumerate(anime.full_stats) if index % 120 == 0 and index < 5000]
    # timestamp = [time for index, time in enumerate(anime.timestamp) if index % 120 == 0 and index < 5000]

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

    #Evaluates Queryset?
    # for index in range(show_list):
    #     show_list[index].decode_name()
    #     pass
    # print(show_list)

    return show_list

def get_shows_search(search_string, genre_bit_sequence, max_shows=50):
    # print(genre_bit_sequence)
    if search_string == '[Query: Genres]':
        if '1' not in genre_bit_sequence:
            return ContentData.objects.order_by('popularity')[:max_shows]
        else:
            show_list = ContentData.objects.order_by('popularity')
            for index, genre_bit in enumerate(genre_bit_sequence):
                if genre_bit == '1':
                    show_list = show_list.filter(genres__icontains=ContentData.show_genres[index])
            num_results = show_list.count() if show_list.count() <= max_shows else max_shows
            show_list = show_list[:num_results]

    else:
        if '1' not in genre_bit_sequence:
            show_list = ContentData.objects.filter(name__icontains=search_string).order_by('popularity')
            num_results = show_list.count() if show_list.count() <= max_shows else max_shows
            show_list = show_list[:num_results]
        else:
            show_list = ContentData.objects.filter(name__icontains=search_string).order_by('popularity')
            for index, genre_bit in enumerate(genre_bit_sequence):
                if genre_bit == '1':
                    show_list = show_list.filter(genres__icontains=ContentData.show_genres[index])
            num_results = show_list.count() if show_list.count() <= max_shows else max_shows
            show_list = show_list[:num_results]

    return show_list

def get_shows_recent(num_shows=5):
    try:
        num_shows_ = int(num_shows)
    except Exception as ex:
        num_shows_ = 5

    today = datetime.date.today()
    three_months_ago = today - datetime.timedelta(days=89)

    today = int(time.mktime(datetime.datetime.strptime(str(today), '%Y-%m-%d').timetuple()))
    three_months_ago = int(time.mktime(datetime.datetime.strptime(str(three_months_ago), '%Y-%m-%d').timetuple()))

    show_list = ContentData.objects.filter(aired__range=(three_months_ago, today)).order_by('-aired')
    show_list = show_list[:num_shows_]

    return show_list

def get_shows_recent_popular(num_shows=5):
    try:
        num_shows_ = int(num_shows)
    except Exception as ex:
        num_shows_ = 5

    today = datetime.date.today()
    three_months_ago = today - datetime.timedelta(days=89)

    today = int(time.mktime(datetime.datetime.strptime(str(today), '%Y-%m-%d').timetuple()))
    three_months_ago = int(time.mktime(datetime.datetime.strptime(str(three_months_ago), '%Y-%m-%d').timetuple()))

    show_list = ContentData.objects.filter(aired__range=(three_months_ago, today)).order_by('popularity')
    show_list = show_list[:num_shows_]
    # print(three_months_ago, today)
    # print(show_list[0].name, show_list[0].aired)

    return show_list

    pass
###################################
# Test methods

def get_show_test2(show_name):
    return [len(show_name) % 12, len(show_name) % 19, len(show_name) % 3, len(show_name) % 5, len(show_name) % 6, len(show_name) % 7]

def get_show_test():
    return [12, 19, 3, 5, 2, 3]

