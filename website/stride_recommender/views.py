from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext


from .getshows import get_shows_random, get_shows_url
from .models import ContentData
from .forms import URLForm

def index(request):
    form = URLForm()
    shows = None
    # request.method should always be POST?

    if request.method == "POST":
        # print('POST request!')
        form = URLForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            shows = get_shows_url(cd.get('url'))
            # return redirect('index')
    else:
        # print('GET request!')
        shows = get_shows_random()

    return render(request, 'recommender.html', {'shows': shows, 'form': form}, RequestContext(request))
