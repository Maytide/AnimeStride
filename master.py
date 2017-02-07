# TODO: Replace ALL references of database in the program to this file
# http://stackoverflow.com/a/32156582

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

# Example of import:

# from django.conf import settings
# sys.path.append(settings.PROJECT_ROOT)
# from master import UNMODELED_DATABASES
# sys.path.remove(settings.PROJECT_ROOT)

UNMODELED_DATABASES = {
    'show_data_individual': {
        'location': os.path.abspath(os.path.join(PROJECT_ROOT,'data/show_data.db')),
    },
    'show_data_aggregated':{
        'location': 'data/show_data_aggregated.db',
    }
}

SHOW_LIST_TYPES = {
    'empty' : 'empty',
    'nonempty' : 'nonempty'
}

# Make this a lot better
def string_SQL_safe(sql_string):
    if 'drop table' not in sql_string:
        return True

    return False