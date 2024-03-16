from django.db import models

class Genre(models.Model):
    title = models.CharField(default = '', max_length = 255)
    description = models.TextField(default='', max_length=1023)

    def __str__(self):
        return self.title