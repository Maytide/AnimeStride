from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import ContentData
from .getshows import get_shows, get_shows_url
from .forms import URLForm

def index(request):
    form = URLForm()
    shows = None
    # request.method should always be POST?

    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            shows = get_shows_url(cd.get('url'))
            # return redirect('index')
    else:
        shows = get_shows()

    return render(request, 'recommender.html', {'shows': shows, 'form': form})
