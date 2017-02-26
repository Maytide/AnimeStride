import json

from django.http import QueryDict
from django.shortcuts import render
from django.views import View

from .getshows import get_shows, get_show_test
from .api import api_get_show_test, api_get_shows_search
from .models import ContentData

# Create your views here.

def index(request):
    show_list = None


    if request.method == "POST":
        # show_list = get_shows(num_shows=10)
        # show_list = get_shows_search()
        process_request(request)
        return api_get_shows_search(request)
    else:
        # print('GET request!')
        show_list = get_shows(num_shows=10)

    return render(request, 'stats.html', {'show_genres': ContentData.show_genres})

def show_stats(request, show_name='Hello'):
    items = get_show_test()

    return render(request, 'stats-page.html', {'shows': items})

def process_request(request):
    if 'application/json' in request.META['CONTENT_TYPE']:
        # load the json data
        # http://stackoverflow.com/questions/24069197/httpresponse-object-json-object-must-be-str-not-bytes
        data = json.loads(request.body.decode())
        # for consistency sake, we want to return
        # a Django QueryDict and not a plain Dict.
        # The primary difference is that the QueryDict stores
        # every value in a list and is, by default, immutable.
        # The primary issue is making sure that list values are
        # properly inserted into the QueryDict.  If we simply
        # do a q_data.update(data), any list values will be wrapped
        # in another list. By iterating through the list and updating
        # for each value, we get the expected result of a single list.
        q_data = QueryDict('', mutable=True)
        # http://stackoverflow.com/questions/30418481/error-dict-object-has-no-attribute-iteritems-when-trying-to-use-networkx
        for key, value in data.items():
            if isinstance(value, list):
                # need to iterate through the list and upate
                # so that the list does not get wrapped in an
                # additional list.
                for x in value:
                    q_data.update({key: x})
            else:
                q_data.update({key: value})

        if request.method == 'GET':
            request.GET = q_data

        if request.method == 'POST':
            request.POST = q_data

    return None