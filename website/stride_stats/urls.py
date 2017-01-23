from django.conf.urls import url
from . import views, api


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^show/(?P<show_name>[a-zA-Z0-9_]+)/$', views.show_stats),
    url(r'^show/api/(?P<show_name>[a-zA-Z0-9_]+)/$', api.api_get_show_stats),
    url(r'^show/test/(?P<show_name>[a-zA-Z0-9_]+)/$', api.api_get_show_test),
    # url(r'^show/api/test/(?P<show_name>[a-zA-Z0-9_]+)/$', api.api_get_show_stats),
]