from django.db import models

class Genre(models.Model):
    genre_id = models.SmallIntegerField()
    title = models.CharField(default = '', max_length = 255)
    description = models.TextField(default='', max_length=1023)