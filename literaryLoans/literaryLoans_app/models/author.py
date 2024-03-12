from django.db import models

class Author(models.Model):
    author_id = models.SmallIntegerField()
    name = models.CharField(default = '', max_length = 255)