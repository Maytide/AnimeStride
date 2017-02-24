import json
from urllib.request import unquote

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

from .getshows import *
from .serializers import *


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class StatisticsContent(object):
    def __init__(self, axis_labels, values):
        self.axis_labels = axis_labels
        self.values = values

# All APIs return two lists: One of axis labels, other of data points (such as members, score, popularity etc)
# Should convert strings to ints
# Should filter out number symbol on popularity
# e.g. '#5' -> 5

def api_get_show_info(request, show_name):
    show = get_show(show_name)

    serializer = ContentDataSerializer(show)
    return JSONResponse(serializer.data)

def api_get_show_stats(request, show_name):
    # test_list = get_show_test()
    # Use unquote to handle special URL characters
    stats_dict, timestamp = get_show_stats(unquote(show_name))

    chart_data = StatisticsContent(timestamp, stats_dict)
    serializer = StatisticsSerializer(chart_data)

    return JSONResponse(serializer.data)
    # return JSONResponse(json.dumps({'values': stats_dict, 'axis_labels': timestamp}))


def api_get_show_basic_stats(request, show_name):
    show = None

    try:
        show = get_show_basic_stats(unquote(show_name))
    except Exception as ex:
        print('[stride_stats: api_get_show_basic_stats] Could not process show.')
        show = {}

    serializer = BasicStatisticsSerializer(show)

    return JSONResponse(serializer.data)

# TODO: fetch ContentData of retrieved recs
def api_get_show_item_rec(request, show_name):
    show = None
    print(show_name)

    try:
        show = get_show_item_rec(unquote(show_name))

    except Exception as ex:
        print('[stride_stats: api_get_show_basic_stats] Could not process show.')
        show = {}

    serializer = ItemRecsSerializer(show)

    return JSONResponse(serializer.data)

def api_get_shows_random(request, num_shows):
    show_list = get_shows_random(num_shows=num_shows)

    serializer = ContentDataSerializer(show_list, many=True)

    return JSONResponse(serializer.data)


def api_get_shows_popularity(request, num_shows):
    show_list = get_shows_popularity(num_shows=num_shows)

    serializer = ContentDataSerializer(show_list, many=True)

    return JSONResponse(serializer.data)

###################################
# Test methods


def api_get_show_test(request, show_name):
    # test_list = get_show_test()
    test_list = get_show_test2(show_name)
    axis_labels = list(range(len(test_list)))

    chart_data = StatisticsContent(axis_labels, test_list)
    serializer = StatisticsSerializer(chart_data)

    return JSONResponse(serializer.data)