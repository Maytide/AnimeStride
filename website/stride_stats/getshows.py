from .models import ContentData


def get_shows(num_shows=10):
    show_list = [ContentData.objects.all()[i] for i in range(num_shows)]
    return show_list

def get_show_stats(show):
    pass


def get_show_test2(show_name):
    return [len(show_name) % 12, len(show_name) % 19, len(show_name) % 3, len(show_name) % 5, len(show_name) % 6, len(show_name) % 7]

def get_show_test():
    return [12, 19, 3, 5, 2, 3]

