from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    url(r'^about/', views.about, name='about'),
    # url(r'^$', views.index, name='index'),
#   url(r'^about/', include(None))
]

urlpatterns += staticfiles_urlpatterns()
