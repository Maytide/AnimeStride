import sys
import os.path
from random import randint

# Navigate to the directory two levels above this one,
# which contains the User class definition in User.py
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..')))
from User import User
# Remove the path after importing is complete.
sys.path.remove(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..')))

from .models import ContentData


def get_shows_random(num_shows=3):
    show_list = [ContentData.objects.all()[randint(0, 1999)] for i in range(num_shows)]
    return show_list

def get_shows_url(url, num_shows=3):
    show_list = [ContentData.objects.all()[len(url)] for i in range(num_shows)]
    return show_list

def get_shows_recommendation(url, num_shows=3):
    user = User()
    user.MAL_URL = url
    user.create_user_show_list_tagged(user.MAL_URL, minimal = True)

    return [ContentData.objects.get(pk = show) for score, show in user.get_user_recommendation(verbose=False)]