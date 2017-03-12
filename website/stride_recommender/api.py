from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import ContentData
from .serializers import ContentDataSerializer, RecommenderSerializer
from .getshows import *
from .forms import URLForm

sys.path.append(settings.PROJECT_ROOT)
from master import string_SQL_safe, SHOW_LIST_TYPES
sys.path.remove(settings.PROJECT_ROOT)

# class ContentDataViewSet(viewsets.ModelViewSet):
#     queryset = ContentData.objects.all().order_by('name')
#     serialzier_class = ContentDataSerializer

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class RecommenderContent(object):
    def __init__(self, list_type, show_list):
        self.rec_type = list_type
        self.rec_list = show_list


def api_get_show_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        show_list = ContentData.objects.all()
        serializer = ContentDataSerializer(show_list, many=True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        show_list = ContentData.objects.all()
        serializer = ContentDataSerializer(show_list, many=True)
        return JSONResponse(serializer.data)

def api_get_show(request, pk):
    show = None
    try:
        show = ContentData.objects.get(pk = pk)
    except show.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ContentDataSerializer(show)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        serializer = ContentDataSerializer(show)
        return JSONResponse(serializer.data)


def api_get_shows_random(request, num_shows=3):
    show_list = get_shows_random(num_shows=num_shows)

    if request.method == 'GET':
        # serializer = ContentDataSerializer(show_list, many=True)
        rec_data = RecommenderContent(SHOW_LIST_TYPES['random'], show_list)
        serializer = RecommenderSerializer(rec_data)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        # serializer = ContentDataSerializer(show_list, many=True)
        rec_data = RecommenderContent(SHOW_LIST_TYPES['random'], show_list)
        serializer = RecommenderSerializer(rec_data)
        return JSONResponse(serializer.data)


# TODO:
# Not working because API has no form!
# How to get form data from webpage to API...
def api_get_shows_url(request, num_shows=3):
    if request.method == 'POST':
        form = URLForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            show_list = get_shows_url(cd.get('url'), num_shows=4)
            serializer = ContentDataSerializer(show_list, many=True)
            # return show_list
        else:
            show_list = get_shows_random(num_shows=10)
            serializer = ContentDataSerializer(show_list, many=True)

        return JSONResponse(serializer.data)
    else:
        show_list = get_shows_random(num_shows=5)
        serializer = ContentDataSerializer(show_list, many=True)
        return JSONResponse(serializer.data)

    ################
    # show_list = None
    # serializer = None
    # # if request.method == 'GET':
    # #     show_list = get_shows_random()
    # #     serializer = ContentDataSerializer(show_list, many=True)
    # #     return ContentDataJSONResponse(serializer.data)
    # # elif request.method == 'POST':
    # form = URLForm(request.POST)
    # if form.is_valid():
    #     cd = form.cleaned_data
    #     show_list = get_shows_url(cd.get('url'))
    #     serializer = ContentDataSerializer(show_list, many=True)
    #
    # return ContentDataJSONResponse(serializer.data)

def api_get_shows_recommendation(request, num_shows=3):
    if request.method == 'POST':
        form = URLForm(request.POST)
        mal_url_start = 'https://myanimelist.net/animelist/'

        if form.is_valid():
            cd = form.cleaned_data
            if cd.get('url')[:len(mal_url_start)] != mal_url_start:
                # list_type, show_list = get_shows_recommendation(cd.get('url'), num_recommendations=4, empty=True, return_empty_state=True)
                list_type, show_list = get_shows_random_popular(return_empty_state=True)
            else:
                list_type, show_list = get_shows_recommendation(cd.get('url'), num_recommendations=4, return_empty_state=True)
            rec_data = RecommenderContent(list_type, show_list)
            # print(show_list)
            # Create special case for this later
            if list_type == SHOW_LIST_TYPES['empty']:
                # serializer = ContentDataSerializer(show_list, many=True)
                serializer = RecommenderSerializer(rec_data)
            elif list_type == SHOW_LIST_TYPES['nonempty']:
                # serializer = ContentDataSerializer(show_list, many=True)
                serializer = RecommenderSerializer(rec_data)
            else:
                serializer = RecommenderSerializer(rec_data)
            # return show_list
        else:
            show_list = get_shows_random(num_shows=10)
            serializer = ContentDataSerializer(show_list, many=True)

        return JSONResponse(serializer.data)
    else:
        show_list = get_shows_random(num_shows=5)
        serializer = ContentDataSerializer(show_list, many=True)
        return JSONResponse(serializer.data)