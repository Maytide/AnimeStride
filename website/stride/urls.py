"""stride URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from stride_recommender import api
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'ContentData', api.ContentDataViewSet)

urlpatterns = [
    # url(r'^', include('home.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^stride_recommender/', include('stride_recommender.urls')),
    url(r'^stride_stats/', include('stride_stats.urls')),
    # Place redirects after everything else, or else
    # Everything matched as redirect
    url(r'^$', RedirectView.as_view(url='/stride_stats/')),
    url(r'^.*/$', RedirectView.as_view(url='/stride_stats/')),
    # url(r'^about/', include(None)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
