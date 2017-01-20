from django.conf.urls import url
from . import views, api

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/random/', api.api_get_shows_random),
    url(r'^api/url/', api.api_get_shows_url),
]