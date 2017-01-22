from django.shortcuts import render
from django.views import View

from .getshows import get_shows, get_show_test
from .api import api_get_show_test

# Create your views here.

def index(request):
    show_list = None
    # request.method should always be POST?

    if request.method == "POST":
        pass
    else:
        # print('GET request!')
        show_list = get_shows(num_shows=10)

    return render(request, 'stats.html', {'shows': show_list})

def show_stats(request, show_name='Hello'):
    items = get_show_test()

    return render(request, 'stats-page.html', {'shows': items})

