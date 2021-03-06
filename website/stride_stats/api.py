import json
from urllib.request import unquote

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

from .getshows import *
from .serializers import *
from .forms import URLForm

sys.path.append(settings.PROJECT_ROOT)
from master import unescape_url_chars, decode_hex_string, EMPTY_CONTENT_DATA
sys.path.remove(settings.PROJECT_ROOT)


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        # print('Stats API JSONResponse:', data)
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class StatisticsContent(object):
    def __init__(self, axis_labels, values):
        self.axis_labels = axis_labels
        self.values = values


class StatisticsContentFull(object):
    def __init__(self, stats_data_month, stats_data_season, stats_data_year, stats_data_all):
        self.stats_data_month = StatisticsContent(stats_data_month['timestamp'], stats_data_month['stats_dict'])
        self.stats_data_season = StatisticsContent(stats_data_season['timestamp'], stats_data_season['stats_dict'])
        self.stats_data_year = StatisticsContent(stats_data_year['timestamp'], stats_data_year['stats_dict'])
        self.stats_data_all = StatisticsContent(stats_data_all['timestamp'], stats_data_all['stats_dict'])


class FrontpageContent(object):
    def __init__(self, show_list_random, show_list_recent, show_list_recent_popular):
        self.show_list_random = show_list_random
        self.show_list_recent = show_list_recent
        self.show_list_recent_popular = show_list_recent_popular

# All APIs return two lists: One of axis labels, other of data points (such as members, score, popularity etc)
# Should convert strings to ints
# Should filter out number symbol on popularity
# e.g. '#5' -> 5


def api_get_show_info(request, show_name):
    show_name_ = unescape_url_chars(show_name)
    show = get_show(show_name_)

    serializer = ContentDataSerializer(show)

    # decode_hex_string(serializer.data)
    return JSONResponse(serializer.data)

def api_get_show_stats(request, show_name):
    # test_list = get_show_test()
    # Use unquote to handle special URL characters
    show_name_ = unescape_url_chars(show_name)
    stats_dict, timestamp = get_show_stats(unquote(show_name_))

    chart_data = StatisticsContent(timestamp, stats_dict)
    serializer = StatisticsSerializer(chart_data)

    return JSONResponse(serializer.data)
    # return JSONResponse(json.dumps({'values': stats_dict, 'axis_labels': timestamp}))


def api_get_show_stats_full(request, show_name):
    show_name_ = unescape_url_chars(show_name)
    try:
        stats_dict_month, timestamp_month = get_show_stats_month(unquote(show_name_))
        stats_dict_season, timestamp_season = get_show_stats_season(unquote(show_name_))
        stats_dict_year, timestamp_year = get_show_stats_year(unquote(show_name_))
        stats_dict_all, timestamp_all = get_show_stats_all(unquote(show_name_))
        # if isinstance(stats_dict_all, list):

    except Exception as ex:
        print('[stride_stats: api_get_show_basic_stats] Could not process show.')
        stats_dict_month, timestamp_month = EMPTY_STATS_DICT['values'], EMPTY_STATS_DICT['axis_labels']
        stats_dict_season, timestamp_season = EMPTY_STATS_DICT['values'], EMPTY_STATS_DICT['axis_labels']
        stats_dict_year, timestamp_year = EMPTY_STATS_DICT['values'], EMPTY_STATS_DICT['axis_labels']
        stats_dict_all, timestamp_all = EMPTY_STATS_DICT['values'], EMPTY_STATS_DICT['axis_labels']



    chart_data = StatisticsContentFull({'stats_dict' : stats_dict_month, 'timestamp' : timestamp_month}, {'stats_dict' : stats_dict_season, 'timestamp' : timestamp_season}
                                   ,{'stats_dict' : stats_dict_year, 'timestamp' : timestamp_year}, {'stats_dict' : stats_dict_all, 'timestamp' : timestamp_all})
    serializer = StatisticsFullSerializer(chart_data)


    return JSONResponse(serializer.data)


def api_get_show_basic_stats(request, show_name):
    show = None
    show_name_ = unescape_url_chars(show_name)

    try:
        show = get_show_basic_stats(unquote(show_name_))
    except Exception as ex:
        print('[stride_stats: api_get_show_basic_stats] Could not process show.')
        show = get_show_basic_stats(EMPTY_CONTENT_DATA)

    serializer = BasicStatisticsSerializer(show)


    return JSONResponse(serializer.data)


# TODO: fetch ContentData of retrieved recs
def api_get_show_item_rec(request, show_name):
    # print('[stride_stats: api_get_show_basic_stats]')
    show_list = None
    show_name_ = unescape_url_chars(show_name)
    # print(show_name)

    try:
        show_list = get_show_item_rec(unquote(show_name_))

    except Exception as ex:
        print('[stride_stats: api_get_show_basic_stats] Could not process show.')

    serializer = ContentDataSerializer(show_list, many=True)
    # decode_hex_string(serializer.data, only_fields=('name'))
    # print(decode_hex_string(serializer.data))
    # decode_hex_string(serializer.data)
    return JSONResponse(serializer.data)


def api_get_shows_random(request, num_shows):
    show_list = get_shows_random(num_shows=num_shows)

    serializer = ContentDataSerializer(show_list, many=True)

    return JSONResponse(serializer.data)


def api_get_shows_popularity(request, num_shows):
    show_list = get_shows_popularity(num_shows=num_shows)

    serializer = ContentDataSerializer(show_list, many=True)

    # decode_hex_string(serializer.data)
    return JSONResponse(serializer.data)


def api_get_shows_search(request):
    # if request.method == 'POST':
    form = URLForm(request.POST)

    print('[Stride Stats: api: api_get_shows_search] Check if form is valid:', form.is_valid())

    if form.is_valid():
        cd = form.cleaned_data
        # print(cd.get('search_string'))
        show_list = get_shows_search(unescape_url_chars(cd.get('search_string')), cd.get('genre_obj'))
        serializer = ContentDataSerializer(show_list, many=True)
    else:
        print('[Stats API api_get_shows_search] error:')
        print(form.errors)
        show_list = get_shows_random(num_shows=2)
        serializer = ContentDataSerializer(show_list, many=True)
    # else:
    #     show_list = get_shows_random(num_shows=3)
    #     serializer = ContentDataSerializer(show_list, many=True)
    # decode_hex_string(serializer.data)
    return JSONResponse(serializer.data)

def api_get_shows_frontpage(request, num_shows=3):
    show_list_random = get_shows_random(num_shows=num_shows)
    show_list_recent = get_shows_recent(num_shows=num_shows)
    show_list_recent_popular = get_shows_recent_popular(num_shows=num_shows)

    frontpage_content = FrontpageContent(show_list_random, show_list_recent, show_list_recent_popular)

    # show_items = {'show_list_recent': show_list_recent, 'show_list_recent_popular': show_list_recent_popular}

    serializer = MultipleContentDataSerializer(frontpage_content)

    # decode_hex_string(serializer.data)
    return JSONResponse(serializer.data)


###################################
# Test methods


def api_get_show_test(request, show_name):
    # test_list = get_show_test()
    test_list = get_show_test2(show_name)
    axis_labels = list(range(len(test_list)))

    chart_data = StatisticsContent(axis_labels, test_list)
    serializer = StatisticsSerializer(chart_data)

    # decode_hex_string(serializer.data)
    return JSONResponse(serializer.data)