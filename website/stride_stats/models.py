from __future__ import unicode_literals

from django.db import models

# (Not used):
# http://stackoverflow.com/questions/37581885/django-using-more-than-one-database-with-inspectdb
# http://stackoverflow.com/questions/4146781/does-a-django-model-know-from-which-database-it-was-loaded-and-how-can-this-info

# Same model and database as stride_recommender app: (Shouldn't be necessary to declare this model twice?)
# Also will use show_data.db with raw SQL Queries

class ContentData(models.Model):
    anime_url = models.TextField(blank=True, null=True)
    name = models.TextField(primary_key=True, blank=True, null=False)
    image_url = models.TextField(default='', blank=True, null=True)
    synopsis = models.TextField(default='', blank=True, null=True)
    english_name = models.TextField(default='', blank=True, null=True)
    synonyms = models.TextField(default='', blank=True, null=True)
    japanese_name = models.TextField(default='', blank=True, null=True)
    media = models.TextField(default='', blank=True, null=True)
    episodes = models.IntegerField(default='', blank=True, null=True)
    aired = models.IntegerField(default='', blank=True, null=True)
    broadcast = models.TextField(default='', blank=True, null=True)
    licensors = models.TextField(default='', blank=True, null=True)
    studios = models.TextField(default='', blank=True, null=True)
    source = models.TextField(default='', blank=True, null=True)
    genres = models.TextField(default='', blank=True, null=True)
    duration = models.TextField(default='', blank=True, null=True)
    rating = models.TextField(default='', blank=True, null=True)
    score = models.FloatField(default='', blank=True, null=True)
    ranked = models.IntegerField(default='', blank=True, null=True)
    members = models.IntegerField(default='', blank=True, null=True)
    popularity = models.IntegerField(default='', blank=True, null=True)
    favourites = models.IntegerField(default='', blank=True, null=True)
    adaptation = models.TextField(default='', blank=True, null=True)
    alternative_version = models.TextField(default='', blank=True, null=True)
    side_story = models.TextField(default='', blank=True, null=True)
    spinoff = models.TextField(default='', blank=True, null=True)
    prequel = models.TextField(default='', blank=True, null=True)
    sequel = models.TextField(default='', blank=True, null=True)
    summary = models.TextField(default='', blank=True, null=True)

    show_genres = ['Action', 'Adventure', 'Comedy', 'Drama', 'Ecchi', 'Fantasy', 'Game', 'Harem', 'Historical', 'Horror',
                'Mecha', 'Military', 'Music', 'Mystery', 'Police', 'Psychological', 'Romance', 'School', 'Sci-Fi', 'Seinen',
                'Shoujo', 'Shounen', 'Slice of Life', 'Space', 'Sports', 'Supernatural']

    class Meta:
        managed = False
        db_table = 'content_data'

    def __str__(self):
        return self.name

    # @staticmethod
    # def get_show_genres():
    #     return show_genresa


class BasicStatistics(models.Model):
    show_name = models.TextField(primary_key=True, blank=True, null=False)
    mean = models.FloatField(blank=True, null=True)
    var = models.FloatField(blank=True, null=True)
    std = models.FloatField(blank=True, null=True)
    rating_zero = models.IntegerField(blank=True, null=True)
    rating_one = models.IntegerField(blank=True, null=True)
    rating_two = models.IntegerField(blank=True, null=True)
    rating_three = models.IntegerField(blank=True, null=True)
    rating_four = models.IntegerField(blank=True, null=True)
    rating_five = models.IntegerField(blank=True, null=True)
    rating_six = models.IntegerField(blank=True, null=True)
    rating_seven = models.IntegerField(blank=True, null=True)
    rating_eight = models.IntegerField(blank=True, null=True)
    rating_nine = models.IntegerField(blank=True, null=True)
    rating_ten = models.IntegerField(blank=True, null=True)
    extra_1 = models.IntegerField(blank=True, null=True)
    extra_2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'basic_statistics'

    def __str__(self):
        return self.show_name

    def get_rating_hist(self):
        return [self.rating_zero, self.rating_one, self.rating_two, self.rating_three,
                self.rating_four, self.rating_five, self.rating_six, self.rating_seven,
                self.rating_eight, self.rating_nine, self.rating_ten]


class ItemRecs(models.Model):
    show_name = models.TextField(primary_key=True, blank=True, null=False)
    rec_1 = models.TextField(blank=True, null=True)
    rec_2 = models.TextField(blank=True, null=True)
    rec_3 = models.TextField(blank=True, null=True)
    rec_4 = models.TextField(blank=True, null=True)
    rec_5 = models.TextField(blank=True, null=True)
    rec_6 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item_recs'

    def __str__(self):
        return self.show_name

    def get_recs(self):
        return [self.rec_1, self.rec_2, self.rec_3, self.rec_4, self.rec_5, self.rec_6]

