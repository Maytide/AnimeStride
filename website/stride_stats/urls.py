from django.conf.urls import url
from . import views, api


# Special characters in URLs:
# http://stackoverflow.com/questions/3675368/django-url-pattern-for-20
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Integer field: \d+
    url(r'^api/popularity/(?P<num_shows>\d+)/$', api.api_get_shows_popularity),
    url(r'^api/random/(?P<num_shows>\d+)/$', api.api_get_shows_random),
    url(r'^api/itemrec/(?P<show_name>[\w|\W]+)/(?P<num_shows>\d+)/$', api.api_get_shows_itemrec),
    url(r'^show/api/1/(?P<show_name>[\w|\W]+)/$', api.api_get_show_stats),
    url(r'^show/api/2/(?P<show_name>[\w|\W]+)/$', api.api_get_show_info),
    url(r'^show/(?P<show_name>[\w|\W]+)/$', views.show_stats),
    # url(r'^show/test/(?P<show_name>[-a-zA-Z0-9_%]+)/$', api.api_get_show_test),
    # url(r'^show/api/test/(?P<show_name>[a-zA-Z0-9_]+)/$', api.api_get_show_stats),
]