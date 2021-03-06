import sys

from django.conf import settings

sys.path.append(settings.PROJECT_ROOT)
from FetchMALData.ReadMALShows import read_MAL_pages
from data.write_extended_stats import write_extended_stats
from data.update_user_data import update_user_data
sys.path.remove(settings.PROJECT_ROOT)


def script_read_MAL_shows(write_individual_entry = True, write_aggregated_entry = False, start_page = 0, start_point = 0, end_page = 40):
    read_MAL_pages(write_individual_entry = write_individual_entry, write_aggregated_entry = write_aggregated_entry, start_page = start_page, start_point = start_point, end_page = end_page, verbose = True)


def script_update_user_data(verbose=True, start_point=0, max_users=10000):
    update_user_data(verbose=verbose, start_point=start_point, max_users=max_users)


def script_write_extended_stats(verbose=False, max_users=1000, max_shows=500, basic_statistics=True, item_rec=True):
    # max_users = 1000
    # max_shows = 500

    write_extended_stats(max_users, max_shows, basic_statistics=basic_statistics, item_rec=item_rec, verbose=verbose)
