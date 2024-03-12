from django.db import models

class Genre(models.Model):
    genre_id = models.SmallIntegerField(default = 0)
    title = models.CharField(default = '', max_length = 255)
    description = models.TextField(default='', max_length=1023)