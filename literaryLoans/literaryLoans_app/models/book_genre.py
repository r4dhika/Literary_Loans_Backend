from django.db import models

# can change the image thing, but for now, it's fine

class BookGenre(models.Model):
    book_id = models.SmallIntegerField(default = 0)
    genre_id = models.SmallIntegerField(default = 0)
