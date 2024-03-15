from django.db import models
from .book import Book
from .genre import Genre

# can change the image thing, but for now, it's fine

class BookGenre(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="books")
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="genres")
