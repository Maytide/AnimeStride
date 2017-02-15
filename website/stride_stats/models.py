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

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'content_data'