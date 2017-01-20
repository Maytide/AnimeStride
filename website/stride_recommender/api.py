from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import ContentData
from .serializers import ContentDataSerializer
from .getshows import get_shows

# class ContentDataViewSet(viewsets.ModelViewSet):
#     queryset = ContentData.objects.all().order_by('name')
#     serialzier_class = ContentDataSerializer

class ContentDataJSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(ContentDataJSONResponse, self).__init__(content, **kwargs)

def api_get_show_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        show_list = ContentData.objects.all()
        serializer = ContentDataSerializer(show_list, many=True)
        return ContentDataJSONResponse(serializer.data)
    elif request.method == 'POST':
        show_list = ContentData.objects.all()
        serializer = ContentDataSerializer(show_list, many=True)
        return ContentDataJSONResponse(serializer.data)

def api_get_show(request, pk):
    show = None
    try:
        show = ContentData.objects.get(pk = pk)
    except show.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ContentDataSerializer(show)
        return ContentDataJSONResponse(serializer.data)

def api_get_shows_random(request, num_shows=3):
    show_list = get_shows(num_shows)

    if request.method == 'GET':
        serializer = ContentDataSerializer(show_list, many=True)
        return ContentDataJSONResponse(serializer.data)
    elif request.method == 'POST':
        serializer = ContentDataSerializer(show_list, many=True)
        return ContentDataJSONResponse(serializer.data)