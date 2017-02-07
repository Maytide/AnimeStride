import sys
import os.path
from random import randint

from django.conf import settings
# Navigate to the directory two levels above this one,
# which contains the User class definition in User.py
# Remove the path after importing is complete.
sys.path.append(settings.PROJECT_ROOT)
from User import User
from master import string_SQL_safe, SHOW_LIST_TYPES
sys.path.remove(settings.PROJECT_ROOT)

from .models import ContentData


def get_shows_random(num_shows=3):
    show_list = [ContentData.objects.all()[randint(0, 1999)] for i in range(num_shows)]
    return show_list

# TODO: Implement method that prevents SQL Injections
def get_shows_url(url, num_shows=3):
    show_list = [ContentData.objects.all()[len(url)] for i in range(num_shows)]
    return show_list

def get_shows_recommendation(url, num_recommendations=3):
    # Measure against SQL Injections:
    if not string_SQL_safe(url):
        return [ContentData.objects.get(pk = 'Boku no Pico') for i in range(num_recommendations)]

    user = User()
    user.MAL_URL = url
    if user.create_user_show_list_tagged(user.MAL_URL, minimal = True):
        return SHOW_LIST_TYPES['nonempty'], [ContentData.objects.get(pk = show) for score, show in
                user.get_user_recommendation(verbose = False, num_recommendations = num_recommendations)]
    else:
        return SHOW_LIST_TYPES['empty'], get_shows_random(num_recommendations)