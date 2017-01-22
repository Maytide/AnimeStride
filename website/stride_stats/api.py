from django.http import HttpResponse

from rest_framework.renderers import JSONRenderer

from .getshows import get_show_test, get_show_test2
from .serializers import StatisticsSerializer, StatisticsListSerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class ChartContent(object):
    def __init__(self, axis_labels, values):
        self.axis_labels = axis_labels
        self.values = values

# All APIs return two lists: One of axis labels, other of data points (such as members, score, popularity etc)
# Should convert strings to ints
# Should filter out number symbol on popularity
# e.g. '#5' -> 5


def api_get_show_test(request, show_name):
    # test_list = get_show_test()
    test_list = get_show_test2(show_name)
    axis_labels = list(range(len(test_list)))

    chart_data = ChartContent(axis_labels, test_list)
    serializer = StatisticsSerializer(chart_data)

    return JSONResponse(serializer.data)