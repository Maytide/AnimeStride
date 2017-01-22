import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from django.template import RequestContext

from .models import ContentData
from .forms import URLForm
from .getshows import get_shows_random, get_shows_url
from .api import api_get_shows_url, api_get_shows_recommendation, api_get_shows_random

# getshows returns list data, while api requires a request and returns json data.

def index(request):
    form = URLForm()
    show_list = None
    # request.method should always be POST?

    if request.method == "POST":
        process_request(request)
        # print('POST request!')
        # form = URLForm(request.POST)
        # if form.is_valid():
        #     cd = form.cleaned_data
        #     show_list = get_shows_url(cd.get('url'))
        #
        #     # return redirect('index')
        #     return show_list
        # return api_get_shows_url(request)
        return api_get_shows_recommendation(request)
    else:
        # print('GET request!')
        show_list = get_shows_random(num_shows=10)
    # RequestContext(request) not needed?
    return render(request, 'recommender.html', {'shows': show_list, 'form': form})

# Error: Pass JSON, expected Querydict
# https://coderwall.com/p/mwhmfg/posting-from-angular-to-django
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