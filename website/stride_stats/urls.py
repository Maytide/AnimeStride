from django.conf.urls import url
from . import views, api


# Special characters in URLs:
# http://stackoverflow.com/questions/3675368/django-url-pattern-for-20
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Integer field: \d+
    url(r'^api/popularity/(?P<num_shows>\d+)/$', api.api_get_shows_popularity),
    url(r'^show/api/(?P<show_name>[\w|\W]+)/$', api.api_get_show_stats),
    url(r'^show/(?P<show_name>[\w|\W]+)/$', views.show_stats),
    # url(r'^show/test/(?P<show_name>[-a-zA-Z0-9_%]+)/$', api.api_get_show_test),
    # url(r'^show/api/test/(?P<show_name>[a-zA-Z0-9_]+)/$', api.api_get_show_stats),
]