# TODO: Replace ALL references of database in the program to this file
# http://stackoverflow.com/a/32156582

import sys
import os
from ast import literal_eval

from urllib.request import unquote


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

# Example of import:

# from django.conf import settings
# sys.path.append(settings.PROJECT_ROOT)
# from master import UNMODELED_DATABASES
# sys.path.remove(settings.PROJECT_ROOT)

japanese_particles = ['no', 'to', 'ni', 'na', 'wa', 'ga']

UNMODELED_DATABASES = {
    'show_data_individual': {
        'location': os.path.abspath(os.path.join(PROJECT_ROOT,'data/show_data_individual.db')),
    },
    'show_data_aggregated': {
        'location': os.path.abspath(os.path.join(PROJECT_ROOT,'data/show_data_aggregated.db')),
    },
    'user_list_indexed': {
        'location': os.path.abspath(os.path.join(PROJECT_ROOT, 'data/user_list_indexed.sqlite3',)),
    },
    'show_indices': {
        'location': os.path.abspath(os.path.join(PROJECT_ROOT,'data/show_indices.db')),
    },
    # for testing only
    # 'show_data_extended': {
    #     'location': os.path.abspath(os.path.join(PROJECT_ROOT,'data/show_data_extended.db')),
    # }
}

SHOW_LIST_TYPES = {
    'empty' : 'empty',
    'nonempty' : 'nonempty',
    'random' : 'random',
    'random-popular' : 'random-popular',
    'popular' : 'popular',
}

EMPTY_STATS_DICT = {
    'axis_labels': {
        'timestamp': [0],
    },
    'values': {
        'score': [-2],
        'favorites': [-2],
        'members': [-2],
        'ranked': [-2],
        'popularity': [-1],
    }
}

EMPTY_BASIC_STATS_DICT = {
    "show_name":"Show not found",
    "mean":-1,
    "var":-1,
    "std":-1,
    'rating_zero': 1,
    'rating_one': 1,
    'rating_two': 1,
    'rating_three': 1,
    'rating_four': 1,
    'rating_five': 1,
    'rating_six': 1,
    'rating_seven': 1,
    'rating_eight': 1,
    'rating_nine': 1,
    'rating_ten': 1,
    'extra_1': 1,
    'extra_2': 1,
}

EMPTY_CONTENT_DATA = 'Show not found'


# See comment above decode_url
def decode_hex_string(item, only_fields=None):
    if isinstance(item, dict):
        for key, value in item.items():
            item[key] = decode_hex_string(item[key])
    elif isinstance(item, list):
        for i in range(len(item)):
            item[i] = decode_hex_string(item[i])
    elif isinstance(item, str):
        try:
            item = literal_eval("b'{}'".format(item)).decode('utf-8')
        except SyntaxError as se:
            # print('[Master decode_hex_string] exception trying to do literal eval', se)
            try:
                item = item.encode('latin-1')
                # print(item)
                item = item.decode('utf-8', 'strict')
            except Exception as ex:
                print('[Master decode_hex_string] exception trying to decode unicode characters')
                print(ex)
                pass
        except Exception as ex:
            pass
        # Printing does not work for special chars?
        # print(item)
    else:
        return item

    return item


# Make this a lot better
def string_SQL_safe(sql_string):
    if 'drop table' not in sql_string:
        return True

    return False


def string_delimiter_upper(lower_string, delimiter, exception_list = None):
    words = lower_string.split(delimiter)
    for index, word in enumerate(words):
        if word not in exception_list:
            words[index] = word[0].upper() + word[1:]

    return ' '.join(words)


# Not encoding my database using utf-8 was a big mistake on my part -
# Now I have to resort to this hack to get my URLs working.
# Take the time to learn urls and encodings properly - it's worth it.
def unescape_url_chars(url):
    url = url.encode('utf-8')
    # print('---------------------------------URL3:', url3)
    url_ = ''

    # for char in url:
    #     if ord(char) > 127:
    #         udata = char.encode('utf-8').decode('latin-1')
    #         for c in udata:
    #             url_ += '\\x' + hex(ord(c))[2:]
    #     else:
    #         url_ += char
    #
    #     # print(char)
    for char in url:
        if char <= 127:
            try:
                url_ += chr(char)
            except Exception as ex:
                pass
        elif char > 127:
            url_ += '\\x' + hex(char)[2:]

    url_ = unquote(url_.replace('[[fsl]]', '/'))

    return url_


def escape_db_string(db_string):
    db_string = db_string.replace(',', '[Comma]')
    db_string = db_string.replace('"', '[Quot]')
    return db_string


def unescape_db_string(db_string):
    db_string = db_string.replace('[Comma]', ',')
    db_string = db_string.replace('[Quot]', '"')
    return db_string