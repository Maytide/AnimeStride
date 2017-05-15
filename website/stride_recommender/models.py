# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


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


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
